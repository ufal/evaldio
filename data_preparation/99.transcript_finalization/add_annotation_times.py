import argparse
from collections import defaultdict
from datetime import datetime, timedelta
import logging
import os
import sys
import xml.etree.ElementTree as ET

ACTION_MAP = {
    "started to edit " : "START",
    "saved changes to  " : "END",
}
DATETIME_FORMAT = "%d/%b/%Y:%I:%M:%S"

def transcript_path2name(path):
    name = os.path.basename(path)
    name_parts = name.split("-")
    # swap the recording name with the annotator's acronym, so that the recording name is first
    if len(name_parts[1]) > len(name_parts[0]):
        name = f"{name_parts[1]}-{name_parts[0]}"
    else:
        name = f"{name_parts[0]}-{name_parts[1]}"
    return name

def parse_userfile(userfile_path):
    userdict = {}
    userfile_doc = ET.parse(userfile_path)
    user_elems = userfile_doc.findall(".//user")
    for user_elem in user_elems:
        userdict[user_elem.attrib["email"]] = user_elem.attrib["short"]
    return userdict

def parse_logfile(logfile, usermap=None):
    logfile_actions = []
    for line in logfile:
        line = line.rstrip()
        fields = line.split("\t")
        if len(fields) < 5:
            continue
        if fields[3] != "wavesurfer":
            continue
        action, filename = None, None
        for action_prefix in ACTION_MAP:
            if fields[4].startswith(action_prefix):
                action = ACTION_MAP[action_prefix]
                filepath = fields[4][len(action_prefix):]
                filename = transcript_path2name(filepath)
        if action is None:
            logging.warning(f"No action for the message: {fields[4]}")
            continue
        user = usermap[fields[1]] if usermap is not None and fields[1] in usermap else fields[1]
        time = datetime.strptime(fields[2], DATETIME_FORMAT)
        logfile_actions.append((time, user, action, filename))
    return logfile_actions

def process_logrecords(log_records):
    duration_dict = defaultdict(lambda: defaultdict(timedelta))
    transcript_starts = defaultdict(dict)
    for time, user, action, filename in log_records:
        if action == "START":
            if user in transcript_starts[filename]:
                prev_time = transcript_starts[filename][user]
                logging.debug(f"[{time}] File {filename} already opened by {user}.")
            transcript_starts[filename][user] = time
        else:
            if user not in transcript_starts[filename]:
                # TEITOK may save the file under the "guest" user even if
                # the original user has been logged out in the meantime.
                # Assign this action to the last user that has opened the file.
                if user != "guest":
                    logging.warning(f"[{time}] Saving file {filename}, which is not yet opened by {user}.")
                    continue
                last_user = max(transcript_starts[filename].keys(), key=lambda x: transcript_starts[filename][x])
                logging.debug(f"[{time}] Saving file {filename} not by {user}, but {last_user}")
                user = last_user
            time_start = transcript_starts[filename][user]
            del transcript_starts[filename][user]
            #if user != user_start:
            #    logging.warning(f"The user who opened and closed {filename} differ: {user_start} {user}")
            #    continue
            duration = time - time_start
            if duration < timedelta():
                logging.debug(f"TIME START: {time_start}")
                logging.debug(f"TIME END: {time}")
                duration += timedelta(hours=12)
                logging.debug(f"DURATION: {duration}")
            elif duration > timedelta(hours=12):
                logging.debug(f"TIME START: {time_start}")
                logging.debug(f"TIME END: {time}")
                duration -= timedelta(hours=12)
                logging.debug(f"DURATION: {duration}")
            duration_dict[filename][user] += duration
    return duration_dict

def insert_time_to_xml(xmltree, duration_time, user=None):
    logging.debug(f"Inserting duration time {duration_time} for the user {user}.")
    header_e = xmltree.find('.//teiHeader')
    transcript_meta_e = header_e.find('./transcriptStmt')
    if transcript_meta_e is None:
        transcript_meta_e = ET.SubElement(header_e, 'transcriptStmt')
    annot_duration_e = ET.Element('annotDuration')
    if user:
        annot_duration_e.attrib["user"] = user
    annot_duration_e.text = str(duration_time)
    transcript_meta_e.append(annot_duration_e)

def main():
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Add duration of the manual annotation to the transcripts' metadata.")
    parser.add_argument('transcript_files', type=str, action="store", nargs="+", help="Transcripts to be extended with the annotation durations.")
    parser.add_argument('--userfile', type=str, help="Path to the file with users, their e-mails and acronyms, which are used in the filenames.")
    parser.add_argument('--author-only', default=False, action="store_true", help="Store only the annotation duration of the transcript's author (identified by the transcript's name)")
    args = parser.parse_args()

    user_email2short = parse_userfile(args.userfile) if args.userfile else None
    #logging.debug(user_email2short)
    
    log_records = parse_logfile(sys.stdin, usermap=user_email2short)
    #logging.debug(log_records)

    durations = process_logrecords(log_records)
    
    #for filename in durations:
    #    for user in durations[filename]:
    #        print("\t".join([filename, user, f"{durations[filename][user]}"]))

    for transcript_path in args.transcript_files:
        transcript_name = transcript_path2name(transcript_path)
        if transcript_name not in durations:
            continue
        logging.debug(f"Processing {transcript_name}")
        transcript_tree = ET.parse(transcript_path)
        for user in durations[transcript_name]:
            if args.author_only and not transcript_name.endswith(f"-{user}"):
                continue
            insert_time_to_xml(transcript_tree, durations[transcript_name][user], user)
        transcript_tree.write(transcript_path, encoding="unicode", xml_declaration=True)

if __name__ == "__main__":
    main()
