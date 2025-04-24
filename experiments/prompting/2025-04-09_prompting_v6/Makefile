SHELL=/bin/bash

TRANSCRIPT_TYPE=whisperX-large-v2
#TRANSCRIPT_TYPE=manual.before_review

BATCH=
BATCH_STR=$(subst $(BATCH),/,-)
TRANSCRIPTS_DIR=../../../tmp/data_preparation/$(BATCH)/01.auto_transcript/$(TRANSCRIPT_TYPE)
LABELS_DIR=../../../tmp/data_preparation/$(BATCH)/20.extract_labels
OUTPUT_DIR=results.$(TRANSCRIPT_TYPE)

SEEDS=42 1986 2025

ALL_BATCHES=UJOP/CCE-A1_2024_06_11 \
            UJOP/CCE-A2_2024_01_26 \
			UJOP/CCE-A2_2024_04_24 \
			UJOP/CCE-A2_older_2025_02_17 \
			UJOP/CCE-B1_2024_05_21 \
			UJOP/CCE-B2_2024_09_23 \
			UJOP/CCE-B2_2025_02_10
# no labels for C1 so far
#			UJOP/CCE-C1_2024_09_23

all :
	for batch in $(ALL_BATCHES); do \
		$(MAKE) prompt_batch BATCH=$$batch TRANSCRIPT_TYPE=$(TRANSCRIPT_TYPE); \
	done

prompt_batch : $(OUTPUT_DIR)/$(BATCH)/llama3.txt $(OUTPUT_DIR)/$(BATCH)/deepseek-r1-70b.txt 

$(OUTPUT_DIR)/$(BATCH)/llama3.txt : MODEL=LLM3-AMD-MI210.llama3.3:latest
$(OUTPUT_DIR)/$(BATCH)/deepseek-r1-70b.txt : MODEL=LLM3-AMD-MI210.deepseek-r1:70b
$(OUTPUT_DIR)/$(BATCH)/llama3.txt $(OUTPUT_DIR)/$(BATCH)/deepseek-r1-70b.txt :
	mkdir -p $(dir $@)
	for labels in $(LABELS_DIR)/*.json; do \
		examid=`basename $$labels | sed 's|_anonym.*||'`; \
		for transcript in $(TRANSCRIPTS_DIR)/$$examid{_,-}*; do \
			python3 prompt.py -m $(MODEL) -r $(SEEDS) -- $$transcript $$labels; \
		done; \
	done > $@
