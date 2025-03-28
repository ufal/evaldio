SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

BATCH_PATH=
SRC_AUDIO_DIR=$(ROOT_DIR)/data/exams/src_audio/$(BATCH_PATH)
TGT_NULL_TRANSCRIPT_DIR=$(ROOT_DIR)/tmp/data_preparation/$(BATCH_PATH)/03.auto_transcripts/null

SRC_AUDIO_FILES=$(wildcard $(SRC_AUDIO_DIR)/*.mp3)
TGT_NULL_TRANSCRIPT_FILES=$(SRC_AUDIO_FILES:$(SRC_AUDIO_DIR)/%.mp3=$(TGT_NULL_TRANSCRIPT_DIR)/%.xml)

######### COMMANDS #########

all : $(TGT_NULL_TRANSCRIPT_FILES)

$(TGT_NULL_TRANSCRIPT_DIR)/%.json : $(SRC_AUDIO_DIR)/%.mp3
	mkdir -p $(dir $@)
	echo "{}" > $@

JSON2TEITOK=../01.transcribe_whisperX/json2teitok.py

$(TGT_NULL_TRANSCRIPT_DIR)/%.xml : $(TGT_NULL_TRANSCRIPT_DIR)/%.json
	mkdir -p $(dir $@)
	python3 $(JSON2TEITOK) $< > $@
