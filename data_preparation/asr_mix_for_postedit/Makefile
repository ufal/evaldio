SHELL=/bin/bash

DATA_DIR=/lnet/ms/data/CoCzeFLA/exams/UJOP/CCE-A2_2024_01_26
SRC_TRANSCRIPTS_DIR=$(DATA_DIR)/03.task2-3_trimmed_transcript
MIXED_TRANSCRIPTS_DIR=$(DATA_DIR)/04.task2-3_mixed_transcripts

all : $(MIXED_TRANSCRIPTS_DIR)/done

$(MIXED_TRANSCRIPTS_DIR)/done :
	mkdir -p $(dir $@)
	for f in $(SRC_TRANSCRIPTS_DIR)/whisperX-large-v2/*.xml; do \
		f=`basename $$f`; \
		python scripts/mix_content.py --seed $$f --fill-empty $(SRC_TRANSCRIPTS_DIR)/*/$$f > $(dir $@)/$$f; \
	done
	touch $@
