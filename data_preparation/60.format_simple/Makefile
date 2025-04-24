SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

BATCH_PATH=
SRC_DIR=$(ROOT_DIR)/tmp/data_preparation/$(BATCH_PATH)/01.auto_transcript/whisperX-large-v2
TGT_DIR=$(ROOT_DIR)/tmp/data_preparation/$(BATCH_PATH)/01.auto_transcript/whisperX-large-v2

SRC_FILES=$(wildcard $(SRC_DIR)/*.xml)
TGT_FILES=$(SRC_FILES:$(SRC_DIR)/%.xml=$(TGT_DIR)/%.simple.txt)

############ RULES ##################

format_simple_all: format_simple_UJOP-CCE-A2_2024_01_26 \
				format_simple_UJOP-CCE-A2_2024_04_24 \
				format_simple_UJOP-CCE-B1_2024_05_21 \
				format_simple_UJOP-CCE-A1_2024_06_11 \
				format_simple_UJOP-CCE-B2_2024_09_23 \
				format_simple_UJOP-CCE-B2_2025_02_10 \
				format_simple_UJOP-CCE-C1_2024_09_23 \
				format_simple_UJOP-sample-2023_02_28 \
				format_simple_UJOP-sample-2023_04_21 \
				format_simple_NPI-sample-2023_02_28 \
				format_simple_NPI-sample-2023_06_30 \
				format_simple_UJOP-CCE-A2_older_2025_02_17

format_simple_UJOP-CCE-A2_2024_01_26:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-A2_2024_01_26
format_simple_UJOP-CCE-A2_2024_04_24:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-A2_2024_04_24
format_simple_UJOP-CCE-B1_2024_05_21:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-B1_2024_05_21
format_simple_UJOP-CCE-A1_2024_06_11:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-A1_2024_06_11
format_simple_UJOP-CCE-B2_2024_09_23:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-B2_2024_09_23
format_simple_UJOP-CCE-B2_2025_02_10:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-B2_2025_02_10
format_simple_UJOP-CCE-C1_2024_09_23:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-C1_2024_09_23
format_simple_UJOP-sample-2023_02_28:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/sample-2023_02_28
format_simple_UJOP-sample-2023_04_21:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/sample-2023_04_21
format_simple_NPI-sample-2023_02_28:
	$(MAKE) format_simple_dir BATCH_PATH=NPI/sample-2023_02_28
format_simple_NPI-sample-2023_06_30:
	$(MAKE) format_simple_dir BATCH_PATH=NPI/sample-2023_06_30
format_simple_UJOP-CCE-A2_older_2025_02_17:
	$(MAKE) format_simple_dir BATCH_PATH=UJOP/CCE-A2_older_2025_02_17

format_simple_dir : $(TGT_FILES)

$(TGT_DIR)/%.simple.txt : $(SRC_DIR)/%.xml
	mkdir -p $(TGT_DIR)
	./format_simple.sh < $< > $@
