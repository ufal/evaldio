SHELL=/bin/bash

BASE_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26

ORIG_AUDIO_DIR=$(BASE_DIR)/00.full_source_audio
ORIG_WHISPERX_DIR=$(BASE_DIR)/01.full_source_transcript_whisperX
SPLIT_AUDIO_DIR=$(BASE_DIR)/02.split_audio

ALL_SRC_FILES=$(wildcard $(ORIG_AUDIO_DIR)/*.mp3)
ALL_TGT_FILES=$(ALL_SRC_FILES:$(ORIG_AUDIO_DIR)/%.mp3=$(SPLIT_AUDIO_DIR)/%.split_done)


all : $(ALL_TGT_FILES)

.PRECIOUS : $(ORIG_WHISPERX_DIR)/%.json $(SPLIT_AUDIO_DIR)/trim_start_times.tsv $(SPLIT_AUDIO_DIR)/%.split_audio
# \ $(TRIMMED_WHISPERX_DIR)/%.json $(TRIMMED_WHISPERX_DIR)/%.xml

# this target requires to be logged in on a machine with a GPU
# need to have the following pyenv activated: /lnet/troja/work/people/mnovak/virtualenvs/evaldio-python3.10-tdll8gpu4
# if "Killed", try changing asking for more memory by calling srun with --mem=50G
# or calling whisperX with float32 replaced by float16, or large-v2 by large-v1, medium, small etc.
$(ORIG_WHISPERX_DIR)/%.json : $(ORIG_AUDIO_DIR)/%.mp3
	mkdir -p $(dir $@)
	whisperx -o=$(dir $@) -f=json --language=cs --model=large-v2 --compute_type=float32 --diarize --hf_token=$(HF_TOKEN) $<

# find times to separate the task 1 from tasks 2 and 3
$(SPLIT_AUDIO_DIR)/trim_start_times.tsv : $(ORIG_WHISPERX_DIR)/*.json
	mkdir -p $(dir $@)
	for f in $^; do \
		echo -en $$f"\t"; \
		jq '.' $$f | \
			grep -P -B2 '"text":.*bude.*[UuÚú]lo' | \
			grep start | \
			head -n1 | \
			sed 's/^.*: \(.*\),$$/\1/'; \
	done > $@ 

$(SPLIT_AUDIO_DIR)/%.split_done : $(ORIG_AUDIO_DIR)/%.mp3 $(SPLIT_AUDIO_DIR)/trim_start_times.tsv
	mkdir -p $(dir $@)
	filename=`basename $(word 1,$^)`; \
	filebase=$${filename%.*}; \
	task2_start_time=`cat $(word 2,$^) | grep "$$filebase" | cut -f2`; \
	task1_filename=`echo $$filename | sed 's/_anonym_audio/_01_anonym_audio/'`; \
	ffmpeg -i $(word 1,$^) -c copy -to $$task2_start_time $(dir $@)/$$task1_filename; \
	task23_filename=`echo $$filename | sed 's/_anonym_audio/_02_anonym_audio/'`; \
	ffmpeg -i $(word 1,$^) -c copy -ss $$task2_start_time $(dir $@)/$$task23_filename; \
	touch $@

# TODO: targets that have not been refactored

TRIMMED_WHISPERX_DIR=$(BASE_DIR)/03.task2-3_trimmed_transcript/whisperX-large-v2

$(TRIMMED_WHISPERX_DIR)/%.json : $(SPLIT_AUDIO_DIR)/%.mp3
	mkdir -p $(dir $@)
	whisperx -o=$(dir $@) -f=json --language=cs --model=large-v2 --compute_type=float32 --diarize --hf_token=$(HF_TOKEN) $<

$(TRIMMED_WHISPERX_DIR)/%.xml : $(TRIMMED_WHISPERX_DIR)/%.json
	mkdir -p $(dir $@)
	python3 scripts/json2teitok.py $< > $@
