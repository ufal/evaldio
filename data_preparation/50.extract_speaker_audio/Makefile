SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..


SRC_AUDIO_BASEDIR=$(ROOT_DIR)/data/exams/src_audio
SRC_TRANS_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/01.auto_transcript/whisperX-large-v2
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/50.extract_speaker_audio/whisperX-large-v2
BATCH_PATH=

SRC_AUDIO_DIR=$(SRC_AUDIO_BASEDIR)/$(BATCH_PATH)
SRC_TRANS_DIR=$(SRC_TRANS_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)

SRC_AUDIO_FILES=$(wildcard $(SRC_AUDIO_DIR)/*.mp3)
SRC_TRANS_FILES=$(SRC_AUDIO_FILES:$(SRC_AUDIO_DIR)/%.mp3=$(SRC_TRANS_DIR)/%.xml)
TGT_MUTED_FILES=$(SRC_AUDIO_FILES:$(SRC_AUDIO_DIR)/%.mp3=$(TGT_DIR)/%.muted.done)

######### COMMANDS #########

$(TGT_DIR)/%.muted.done : $(SRC_AUDIO_DIR)/%.mp3 $(SRC_TRANS_DIR)/%.xml
	mkdir -p $(dir $@)
	python3 speaker_ffmpeg_cmd.py $(word 2,$^) | \
		while IFS=$$'\t' read -r speaker ffmpeg_cmd; do \
			donef="$@"; \
			outf=$${donef%.done}.speaker-$$speaker.mp3; \
			eval ffmpeg -i $(word 1,$^) $$ffmpeg_cmd $$outf < /dev/null; \
		done
	touch $@

speakers_muted : $(TGT_MUTED_FILES)
