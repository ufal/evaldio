SHELL=/bin/bash

# TODO: not yet tested

VENV=/lnet/troja/work/people/mnovak/virtualenvs/evaldio-python3.10-tdll8gpu4
WHISPERX=. $(VENV)/bin/activate; whisperx

SRC_DIR=
TGT_DIR=

SRC_FILES:=$(SRC_DIR)/*.mp3

###### PREREQUISITIES ######
# 1. log in to a GPU machine
# 2. set your Hugging Face token by running
#		export HF_TOKEN=???

transcribe_all: transcribe_UJOP-CCE-A2_2024_01_26 transcribe_UJOP-CCE-A2_2024_04_24

transcribe_UJOP-CCE-A2_2024_01_26:
	make transcribe_dir SRC_DIR=data/exams/UJOP/CCE-A2_2024_01_26 TGT_DIR=tmp/data_preparation/UJOP/CCE-A2_2024_01_26
transcribe_UJOP-CCE-A2_2024_04_24:
	make transcribe_dir SRC_DIR=data/exams/UJOP/CCE-A2_2024_04_24 TGT_DIR=tmp/data_preparation/UJOP/CCE-A2_2024_04_24

transcribe_dir: $(TGT_DIR)/done
$(TGT_DIR)/done :
	mkdir -p $(TGT_DIR)
	$(WHISPERX) \
		-o=$(TGT_DIR)
		-f=json \
		--language=cs \
		--model=large-v2 \
		--compute_type=float32 \
		--diarize \
		--hf_token=$(HF_TOKEN) \
		$(SRC_FILES)
	touch $@
