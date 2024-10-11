SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/data/exams/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/01.auto_transcript/whisperX-large-v2
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)

SRC_FILES=$(wildcard $(SRC_DIR)/*.mp3)
TGT_FILES=$(SRC_FILES:$(SRC_DIR)/%.mp3=$(TGT_DIR)/%.xml)

####### PROCESSING VARIABLES #####

VENV=/lnet/troja/work/people/mnovak/virtualenvs/evaldio-python3.10-tdll8gpu4
WHISPERX=. $(VENV)/bin/activate; whisperx

###### PREREQUISITIES ######
# 1. log in to a GPU machine
# 2. set your Hugging Face token by running
#		export HF_TOKEN=???
# 3. if "Killed", try asking for more memory by calling srun with --mem=50G (alternatively by calling whisperX with float32 replaced by float16, or large-v2 by large-v1, medium, small etc.)

transcribe_all: transcribe_UJOP-CCE-A2_2024_01_26 \
				transcribe_UJOP-CCE-A2_2024_04_24 \
				transcribe_UJOP-CCE-B1_2024_05_21 \
				transcribe_UJOP-CCE-A1_2024_06_11 \
				transcribe_UJOP-CCE-B2_2024_09_23 \
				transcribe_UJOP-CCE-C1_2024_09_23 \
				transcribe_UJOP-sample-2023_02_28 \
				transcribe_UJOP-sample-2023_04_21 \
				transcribe_NPI-sample-2023_02_28 \
				transcribe_NPI-sample-2023_06_30

transcribe_UJOP-CCE-A2_2024_01_26:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/CCE-A2_2024_01_26
transcribe_UJOP-CCE-A2_2024_04_24:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/CCE-A2_2024_04_24
transcribe_UJOP-CCE-B1_2024_05_21:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/CCE-B1_2024_05_21
transcribe_UJOP-CCE-A1_2024_06_11:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/CCE-A1_2024_06_11
transcribe_UJOP-CCE-B2_2024_09_23:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/CCE-B2_2024_09_23
transcribe_UJOP-CCE-C1_2024_09_23:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/CCE-C1_2024_09_23
transcribe_UJOP-sample-2023_02_28:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/sample-2023_02_28
transcribe_UJOP-sample-2023_04_21:
	$(MAKE) transcribe_dir BATCH_PATH=UJOP/sample-2023_04_21
transcribe_NPI-sample-2023_02_28:
	$(MAKE) transcribe_dir BATCH_PATH=NPI/sample-2023_02_28
transcribe_NPI-sample-2023_06_30:
	$(MAKE) transcribe_dir BATCH_PATH=NPI/sample-2023_06_30

.PRECIOUS : $(TGT_DIR)/%.json

transcribe_dir: $(TGT_FILES)
$(TGT_DIR)/%.json : $(SRC_DIR)/%.mp3
	mkdir -p $(TGT_DIR)
	$(WHISPERX) \
		-o=$(TGT_DIR) \
		-f=json \
		--language=cs \
		--model=large-v2 \
		--compute_type=float32 \
		--diarize \
		--hf_token=$(HF_TOKEN) \
		$<

$(TGT_DIR)/%.xml : $(TGT_DIR)/%.json
	python3 json2teitok.py $< | \
		python3 normalize.py | \
		xmllint --format - > $@
