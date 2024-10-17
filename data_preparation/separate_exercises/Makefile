SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/separate_exercises
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)

# the set of audio recordings to be verified is given by the *.split_times.txt files
SPLIT_TIME_FILES=$(wildcard $(TGT_DIR)/*.split_times.txt)
SRC_FILES=$(SPLIT_TIME_FILES:$(TGT_DIR)/%.split_times.txt=$(SRC_DIR)/%.mp3)
TGT_FILES=$(SRC_FILES:$(SRC_DIR)/%.mp3=$(TGT_DIR)/%.verify_split.mp3)


########### VERIFICATION OF SPLIT TIMES #############

EXCERPT_HALFLENGTH=3

verify_split : $(TGT_FILES)

beep.mp3 :
	ffmpeg -f lavfi -i "sine=frequency=1000:duration=0.05" $@

# for the time being, there must be a single split timestamp in each *.split_times.txt file
$(TGT_DIR)/%.verify_split.mp3 : $(SRC_DIR)/%.mp3 $(TGT_DIR)/%.split_times.txt beep.mp3
	mkdir -p $(TGT_DIR)
	split_time=`cat $(word 2,$^)`; \
	start_time=`echo $$split_time - $(EXCERPT_HALFLENGTH) | bc`; \
	end_time=`echo $$split_time + $(EXCERPT_HALFLENGTH) | bc`; \
	ffmpeg -i $(word 1,$^) -ss $$start_time -to $$end_time -c copy $(TGT_DIR)/$*.excerpt.mp3; \
	ffmpeg -i $(TGT_DIR)/$*.excerpt.mp3 -i beep.mp3 -filter_complex \
		"[1:a]adelay=$(EXCERPT_HALFLENGTH)000|$(EXCERPT_HALFLENGTH)000[b]; [0:a][b]amix=inputs=2" \
		-c:a libmp3lame -q:a 2 $@; \
	rm $(TGT_DIR)/$*.excerpt.mp3

########### TEMPORARY RULES TO GENERATE SPLIT TIMES #############
# for the time being, the split ranges have been selected manually
# they should be extracted automatically in the future

release_A2_202410.split_times.csv : release_A2_202410.split_time_ranges.csv
	python3 time_ranges_to_times.py < $< > $@

$(TGT_DIR)/split_times.done : release_A2_202410.split_times.csv
	cat $< | while read fid t; do \
		if [[ -z "$$t" ]]; then \
			continue; \
		fi; \
		bfaudio=`ls $(SRC_DIR)/*$$fid* | head -n1 | xargs basename`; \
		bf=$${bfaudio%.mp3}.split_times.txt; \
		echo "$$t" > $(dir $@)/$$bf; \
	done
	touch $@
