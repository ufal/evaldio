""" Add a proper TEI header to the input file """
import argparse
from datetime import datetime
import os
import re
import xml.etree.ElementTree as ET

TEI_HEADER_TEMPLATE = """
<teiHeader>
  <fileDesc>
    <titleStmt>
      <title lang="cs">Databáze mluvených projevů v češtině jako cizím jazyce (trvalý pobyt v ČR), zkouška {examid}, úloha {exerno}, přepis {annotator_short}</title>
      <title lang="en">Database of Spoken Czech as a Foreign Language (Permanent Residency in the Czech Republic), Exam {examid}, Task {exerno}, Transcript {annotator_short}</title>
      <respStmt>
        <resp lang="en">Authors and maintainers</resp>
        <name>Kateřina Rysová</name>
        <name>Michal Novák</name>
        <name>Magdaléna Rysová</name>
        <name>Peter Polák</name>
        <name>Ondřej Bojar</name>
        <orgName lang="cs">Ústav formální a aplikované lingvistiky, Matematicko-fyzikální fakulta, Univerzita Karlova</orgName>
        <orgName lang="en">Institute of Formal and Applied Linguistics, Faculty of Mathematics and Physics, Charles University</orgName>
      </respStmt>
      <respStmt>
        <resp lang="en">Author of the recording</resp>
        <orgName lang="cs">{rec_inst}</orgName>
        <orgName lang="en">{rec_inst_en}</orgName>
      </respStmt>
      <respStmt>
        <resp lang="en">Annotator</resp>
        <name>{annotator}</name>
      </respStmt>
      <respStmt>
        <resp lang="en">Reviewer</resp>
        <name>{reviewer}</name>
      </respStmt>
    </titleStmt>

    <editionStmt>
      <edition>{pub_version}</edition>
    </editionStmt>

    
    <publicationStmt>
      <!-- <publisher>Ústav formální a aplikované lingvistiky</publisher>
            <pubPlace>Prague, Czech Republic</pubPlace> -->
      <publisher>
        <orgName lang="cs">LINDAT/CLARIAH-CZ: Digitální výzkumná infrastruktura pro jazykové technologie, umění a humanitní vědy</orgName>
        <orgName lang="en">LINDAT/CLARIAH-CZ: Digital Research Infrastructure for Language Technologies, Arts and Humanities</orgName>
        <ref target="https://www.lindat.cz">www.lindat.cz</ref>
      </publisher>
      <idno type="URI" subtype="handle">{handle_uri}</idno>
      <availability status="free">
        <licence>https://creativecommons.org/licenses/by-nc-sa/4.0/</licence>
        <p lang="en">This work is licensed under the <ref target="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)</ref>.</p>
      </availability>  
      <date when="{pub_date:%Y-%m-%d}">{pub_date:%d.%m.%Y}</date>
    </publicationStmt>
    
    <sourceDesc>
      <bibl>
        <title type="main" lang="cs">Certifikovaná zkouška z češtiny pro cizince, úroveň {level}, ústní část, úloha {exerno}</title>
        <title type="main" lang="en">Czech Language Certificate Exam, {level} Level, Oral Part, Task {exerno}</title>
        <author lang="cs">{rec_inst}</author>
        <author lang="en">{rec_inst_en}</author>
        <date when="{rec_date:%Y-%m-%d}">{rec_date:%d.%m.%Y}</date>
      </bibl>
      <recordingStmt>
        <recording>
          <media url="{recording_path}"/>
        </recording>
      </recordingStmt>
    </sourceDesc>
  </fileDesc>
  
  <encodingDesc>
    <projectDesc>
      <p lang="en"><ref target="https://ufal.mff.cuni.cz/evaldio">Evaldio</ref> is a project that aims to design and implement software applications for the automatic evaluation of spoken Czech produced by students of Czech as a foreign language who are preparing for certified language exams.</p>
    </projectDesc>
    
    <annotationDecl>
      <desc lang="en">Annotation of the recordings that consists of: transcripts, time-alignment on the utterance level, assignment of speakers to utterances, tokenization of transcripts, token-level linguistic annotation</desc>
      <annotation>
        <respStmt>
          <resp lang="en">Annotator</resp>
          <name>{annotator}</name>
          <desc>Pre-annotation source: {preannot_source}.</desc>
        </respStmt>
      </annotation>
      <annotation>
        <respStmt>
          <resp lang="en">Reviewer</resp>
          <name>{reviewer}</name>
        </respStmt>
      </annotation>
    </annotationDecl>
  </encodingDesc>
  
  <profileDesc>
    <langUsage>
      <language ident="ces">Czech</language>
    </langUsage>
    <textClass>
      <keywords scheme="custom">
        <term type="cefr-level">{level}</term>
        <term type="task-number">{exerno}</term>
        <term type="preannot-source">{type}</term>
      </keywords>
      <classCode scheme="custom">{level}.task{exerno}.{type}</classCode>
    </textClass>
  </profileDesc>
</teiHeader>
"""

ANNOTATOR_NAMES = {
    'AP': 'Anna Pánková',
    'ET': 'Ester Tichá',
    'KV': 'Klára Vučičová',
    'LR': 'Ludmila Rosenbaumová',
    'ZM': 'Zuzana Míšková',
    'MH': 'Martina Hulešová',
    'KR': 'Kateřina Rysová',
    'MR': 'Magdaléna Rysová',
}

PREANNOT_SOURCE_NAMES = {
    'from_scratch': 'No pre-annotation',
    'from_whisperX': 'WhisperX (annotator post-edited ASR output)',
    'from_mixed': 'multiple ASR systems (annotator post-edited ASR output)',
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to the input file')
    parser.add_argument('output', help='Path to the output file')
    parser.add_argument('--pub-date', type=str, default='2024-10-31', help='Publication date')
    parser.add_argument('--pub-version', type=str, default='1.0', help='Publication version')
    parser.add_argument('--handle-uri', type=str, default='http://hdl.handle.net/11234/1-5731', help='Handle URI')
    parser.add_argument('--rec-inst', type=str, default='Ústav jazykové a odborné přípravy Univerzity Karlovy', help='Name of the institution that made the recording')
    parser.add_argument('--rec-inst-en', type=str, default='Institute of Language and Preparatory Studies of Charles University', help='Name of the institution that made the recording in English')
    parser.add_argument('--rec-inst-short', type=str, default='ÚJOP', help='Short name of the institution that made the recording')
    return parser.parse_args()

def add_info_from_filename(info, filename):
    basename = os.path.basename(filename)
    # parse the filenames such as A2ML_221205_18_02-AP-from_scratch.exer3.xml, where
    # "A2" is the CEFR level
    # "221205" is the exam date
    # "18" is the exam number
    # "AP" is the acronym of the annotator
    # "from_scratch" refers to the the source of pre-annotation, here there was no pre-annotation
    # "exer3" is the task number
    match = re.match(r'(?P<level>[A-C][1-2])ML_(?P<rec_date>\d{6})_(?P<examno>\d{2}).*-(?P<annotator_short>\w{2})-(?P<type>\w+)-exer(?P<exerno>[1-9])\.xml', basename)
    if not match:
        return None
    info.update(match.groupdict())
    # convert the annotator acronym to the full name
    info['annotator'] = ANNOTATOR_NAMES[info['annotator_short']]
    info['examid'] = f"{info['rec_inst_short']}-{info['level']}-{info['rec_date']}_{info['examno']}"
    info['rec_date'] = datetime.strptime(info['rec_date'], '%y%m%d')
    info['preannot_source'] = PREANNOT_SOURCE_NAMES[info['type']]

def add_info_from_file_content(info, doctree):
    # add the recording path and duration
    info['recording_path'] = doctree.find('.//media').attrib['url']
    #info['recording_duration'] = doctree.find('.//recording').attrib['dur']

    # add the annotation duration information
    annot_duration_elems = doctree.findall('.//annotDuration')
    annot_primary_duration_elems = [elem for elem in annot_duration_elems if elem.attrib.get('user') == info['annotator_short']]
    assert len(annot_primary_duration_elems) <= 1, f"Expected at most one primary annotation duration, got {len(annot_primary_duration_elems)}"
    info['annot_duration'] = annot_primary_duration_elems[0].text if annot_primary_duration_elems else None
    info['annot_duration_approx'] = bool(annot_primary_duration_elems[0].attrib.get('approx', '0')) if annot_primary_duration_elems else None
    review_duration_elems = [elem for elem in annot_duration_elems if elem.attrib.get('user') != info['annotator_short']]
    assert len(review_duration_elems) <= 1, f"Expected at most one review annotation duration, got {len(review_duration_elems)}"
    info['review_duration'] = review_duration_elems[0].text if review_duration_elems else None
    info['review_duration_approx'] = bool(review_duration_elems[0].attrib.get('approx', '0')) if review_duration_elems else None
    info['reviewer'] = ANNOTATOR_NAMES[review_duration_elems[0].attrib.get('user') if review_duration_elems else 'MR']

def add_info_from_args(info, args):
    for name in ['handle_uri', 'pub_version', 'rec_inst', 'rec_inst_en', 'rec_inst_short']:
        info[name] = getattr(args, name)
    info['pub_date'] = datetime.strptime(args.pub_date, '%Y-%m-%d')

def replace_tei_header(doctree, info):
    # delete the old header
    old_header_elem = doctree.find('.//teiHeader')
    if old_header_elem is not None:
        doctree.getroot().remove(old_header_elem)
    # format and add the new header    
    tei_header_str = TEI_HEADER_TEMPLATE.format(**info)
    tei_header_elem = ET.fromstring(tei_header_str)
    doctree.getroot().insert(0, tei_header_elem)

def main():
    args = parse_args()
    doctree = ET.parse(args.input)
    # collect the information for the TEI header
    info = {}
    add_info_from_args(info, args)
    add_info_from_filename(info, args.input)
    add_info_from_file_content(info, doctree)
    # write the file with a new header
    replace_tei_header(doctree, info)
    doctree.write(args.output, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    main()