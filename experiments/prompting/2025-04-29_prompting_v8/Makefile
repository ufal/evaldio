SHELL=/bin/bash

BATCH=
BATCH_STR=$(subst $(BATCH),/,-)
TRANSCRIPTS_DIR=../../../tmp/data_preparation/$(BATCH)/01.auto_transcript/whisperX-large-v2
LABELS_DIR=../../../tmp/data_preparation/$(BATCH)/20.extract_labels
OUTPUT_DIR=results

SEEDS=42

ALL_BATCHES=UJOP/CCE-A1_2024_06_11 \
            UJOP/CCE-A2_2024_01_26 \
			UJOP/CCE-A2_2024_04_24 \
			UJOP/CCE-A2_older_2025_02_17 \
			UJOP/CCE-B1_2024_05_21 \
			UJOP/CCE-B2_2024_09_23 \
			UJOP/CCE-B2_2025_02_10
# no labels for C1 so far
#			UJOP/CCE-C1_2024_09_23

all_llama :
	for batch in $(ALL_BATCHES); do \
		$(MAKE) prompt_batch_llama BATCH=$$batch; \
	done

all_deepseek :
	for batch in $(ALL_BATCHES); do \
		$(MAKE) prompt_batch_deepseek BATCH=$$batch; \
	done

prompt_batch_llama : $(OUTPUT_DIR)/$(BATCH)/llama3.txt
prompt_batch_deepseek : $(OUTPUT_DIR)/$(BATCH)/deepseek-r1-70b.txt 

$(OUTPUT_DIR)/$(BATCH)/llama3.txt : MODEL=LLM3-AMD-MI210.llama3.3:latest
$(OUTPUT_DIR)/$(BATCH)/deepseek-r1-70b.txt : MODEL=LLM3-AMD-MI210.deepseek-r1:70b
$(OUTPUT_DIR)/$(BATCH)/llama3.txt $(OUTPUT_DIR)/$(BATCH)/deepseek-r1-70b.txt :
	mkdir -p $(dir $@)
	for labels in $(LABELS_DIR)/*.json; do \
		base=`basename $$labels .json`; \
		transcript=$(TRANSCRIPTS_DIR)/$$base.simple.txt; \
		python3 prompt.py -m $(MODEL) -r $(SEEDS) -o $(dir $@)/$$base -- $$transcript; \
	done > $@
