SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

BATCH_PATH=
SRC_AUDIO_DIR=$(ROOT_DIR)/data/exams/src_audio/$(BATCH_PATH)
SRC_TRANS_DIR=$(ROOT_DIR)/tmp/data_preparation/$(BATCH_PATH)/01.auto_transcript/whisperX-large-v2
TGT_DIR=$(ROOT_DIR)/tmp/data_preparation/$(BATCH_PATH)/50.extract_speaker_audio/whisperX-large-v2

SRC_AUDIO_FILES=$(wildcard $(SRC_AUDIO_DIR)/*.mp3)
SRC_TRANS_FILES=$(SRC_AUDIO_FILES:$(SRC_AUDIO_DIR)/%.mp3=$(SRC_TRANS_DIR)/%.xml)
TGT_MUTED_FILES=$(SRC_AUDIO_FILES:$(SRC_AUDIO_DIR)/%.mp3=$(TGT_DIR)/%.muted.done)
TGT_DELETED_FILES=$(SRC_AUDIO_FILES:$(SRC_AUDIO_DIR)/%.mp3=$(TGT_DIR)/%.deleted.done)

######### COMMANDS #########

$(TGT_DIR)/%.muted.done : FLAG=--join-neighbours
$(TGT_DIR)/%.deleted.done : FLAG=--delete --join-neighbours
$(TGT_DIR)/%.muted.done $(TGT_DIR)/%.deleted.done : $(SRC_AUDIO_DIR)/%.mp3 $(SRC_TRANS_DIR)/%.xml
	mkdir -p $(dir $@)
	python3 speaker_ffmpeg_cmd.py $(FLAG) $(word 2,$^) | \
		while IFS=$$'\t' read -r speaker ffmpeg_cmd; do \
			donef="$@"; \
			outf=$${donef%.done}.speaker-$$speaker.mp3; \
			eval ffmpeg -i $(word 1,$^) $$ffmpeg_cmd $$outf < /dev/null; \
		done
	touch $@

speakers_muted : $(TGT_MUTED_FILES)
speakers_deleted : $(TGT_DELETED_FILES)
