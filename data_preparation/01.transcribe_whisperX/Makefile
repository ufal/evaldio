SHELL=/bin/bash
MAKEFILE_PATH:=$(lastword $(MAKEFILE_LIST))

####### DIR VARIABLES #######

SRC_BASEDIR=data/exams
TGT_BASEDIR=tmp/data_preparation/01.auto_transcript/whisperX-large-v2
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)

SRC_FILES=$(wildcard $(SRC_DIR)/*.mp3)
TGT_FILES=$(SRC_FILES:$(SRC_DIR)/%.mp3=$(TGT_DIR)/%.json)

####### PROCESSING VARIABLES #####

VENV=/lnet/troja/work/people/mnovak/virtualenvs/evaldio-python3.10-tdll8gpu4
WHISPERX=. $(VENV)/bin/activate; whisperx

###### PREREQUISITIES ######
# 1. log in to a GPU machine
# 2. set your Hugging Face token by running
#		export HF_TOKEN=???
# 3. if "Killed", try asking for more memory by calling srun with --mem=50G (alternatively by calling whisperX with float32 replaced by float16, or large-v2 by large-v1, medium, small etc.)

transcribe_all: transcribe_UJOP-CCE-A2_2024_01_26 transcribe_UJOP-CCE-A2_2024_04_24

transcribe_UJOP-CCE-A2_2024_01_26:
	$(MAKE) -f $(MAKEFILE_PATH) transcribe_dir BATCH_PATH=UJOP/CCE-A2_2024_01_26
transcribe_UJOP-CCE-A2_2024_04_24:
	$(MAKE) -f $(MAKEFILE_PATH) transcribe_dir BATCH_PATH=UJOP/CCE-A2_2024_04_24

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
