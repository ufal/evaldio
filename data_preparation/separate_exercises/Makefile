SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/separate_exercises
SRC_ANNOT_BASEDIR=$(ROOT_DIR)/redmine_data/final/transcripts/manual
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)
SRC_ANNOT_DIR=$(SRC_ANNOT_BASEDIR)

# the set of audio recordings to be verified is given by the *.split_times.txt files
SPLIT_TIME_FILES=$(wildcard $(TGT_DIR)/*.split_times.txt)
SRC_FILES=$(SPLIT_TIME_FILES:$(TGT_DIR)/%.split_times.txt=$(SRC_DIR)/%_anonym_audio.mp3)
VERIFICATION_FILES=$(SPLIT_TIME_FILES:$(TGT_DIR)/%.split_times.txt=$(TGT_DIR)/%.verify_split.done)
TGT_AUDIO_DONE_FILES=$(SPLIT_TIME_FILES:$(TGT_DIR)/%.split_times.txt=$(TGT_DIR)/%.audio_split.done)

TGT_ANNOT_DONE_FILES=$(SPLIT_TIME_FILES:$(TGT_DIR)/%.split_times.txt=$(TGT_DIR)/%.all_annot_split.done)

########### SPLIT OF RECORDINGS ############

split_audio : $(TGT_AUDIO_DONE_FILES)

$(TGT_DIR)/%.audio_split.done : $(SRC_DIR)/%_anonym_audio.mp3 $(TGT_DIR)/%.split_times.txt
	mkdir -p $(TGT_DIR)
	./split_audio_by_times.sh $(word 1,$^) $(word 2,$^) $(dir $@)
	touch $@

########### SPLIT OF ANNOTATIONS ############

split_annotations : $(TGT_ANNOT_DONE_FILES)

$(TGT_DIR)/%.all_annot_split.done : $(TGT_DIR)/%.split_times.txt
	mkdir -p $(TGT_DIR)
	for f in `ls $(SRC_ANNOT_DIR)/*$**.xml`; do \
		bf=`basename $$f .xml`; \
		$(MAKE) $(TGT_DIR)/$$bf.annot_split.done SPLIT_TIMES_FILE=$<; \
	done
	touch $@

$(TGT_DIR)/%.annot_split.done : $(SRC_ANNOT_DIR)/%.xml
	mkdir -p $(TGT_DIR)
	python3 split_transcripts_by_times.py \
		--output-prefix $(TGT_DIR)/$* \
		`cat $(SPLIT_TIMES_FILE)` \
		< $<
	touch $@

########### VERIFICATION OF SPLIT TIMES #############

EXCERPT_HALFLENGTH=3

verify_splits : $(VERIFICATION_FILES)

beep.mp3 :
	ffmpeg -f lavfi -i "sine=frequency=1000:duration=0.05" $@

# for the time being, there must be a single split timestamp in each *.split_times.txt file
$(TGT_DIR)/%.verify_split.done : $(SRC_DIR)/%_anonym_audio.mp3 $(TGT_DIR)/%.split_times.txt beep.mp3
	mkdir -p $(TGT_DIR)
	./verify_split.sh $(word 1,$^) $(word 2,$^) $(EXCERPT_HALFLENGTH) $(TGT_DIR)/$*
	touch $@

########### TEMPORARY RULES TO GENERATE SPLIT TIMES #############
# for the time being, the split ranges have been selected manually
# they should be extracted automatically in the future

release_A2_202410.split_times.csv : release_A2_202410.split_time_ranges.csv
	python3 time_ranges_to_times.py < $< > $@

$(TGT_DIR)/split_times.done : release_A2_202410.split_times.csv
	cat $< | while read fid split_info; do \
		echo "$$split_info" | sed 's/ /\n/g' > $(dir $@)/$$fid.split_times.txt; \
	done
	touch $@
