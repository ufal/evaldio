SHELL=/bin/bash

BASE_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26

SPLIT_AUDIO_DIR=$(BASE_DIR)/02.split_audio
NULL_TRANSCRIPT_DIR=$(BASE_DIR)/03.auto_transcripts/null

ALL_SRC_FILES=$(wildcard $(SPLIT_AUDIO_DIR)/*.mp3)
ALL_TGT_FILES=$(ALL_SRC_FILES:$(SPLIT_AUDIO_DIR)/%.mp3=$(NULL_TRANSCRIPT_DIR)/%.xml)

all : $(ALL_TGT_FILES)

$(NULL_TRANSCRIPT_DIR)/%.json : $(SPLIT_AUDIO_DIR)/%.mp3
	mkdir -p $(dir $@)
	echo "{}" > $@

JSON2TEITOK=../01.transcribe_whisperX/json2teitok.py

$(NULL_TRANSCRIPT_DIR)/%.xml : $(NULL_TRANSCRIPT_DIR)/%.json
	mkdir -p $(dir $@)
	python3 $(JSON2TEITOK) $< > $@
