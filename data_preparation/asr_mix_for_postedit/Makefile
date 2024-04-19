SHELL=/bin/bash

DATA_DIR=/lnet/ms/data/CoCzeFLA/exams/UJOP/CCE-A2_2024_01_26
SRC_DIR=$(DATA_DIR)/03.task2-3_trimmed_transcript
TGT_DIR=$(DATA_DIR)/04.task2-3_mixed_transcripts

all : $(TGT_DIR)/done

$(TGT_DIR)/done :
	mkdir -p $(dir $@)
	for f in $(SRC_DIR)/whisperX-large-v2/*.xml; do \
		f=`basename $$f`; \
		logf=$${f%.xml}.log; \
		scripts/mix_content.py --seed $$f --fill-empty $(SRC_DIR)/*/$$f 2>&1 > $(dir $@)/$$f | tee $(dir $@)/$$logf; \
	done
	touch $@

clean :
	rm -rf $(TGT_DIR)
