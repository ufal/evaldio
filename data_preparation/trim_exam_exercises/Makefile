SHELL=/bin/bash

BASE_DIR=/lnet/ms/data/CoCzeFLA/exams/UJOP/CCE-A2_2024_01_26

ORIG_AUDIO_DIR=$(BASE_DIR)/00.source_audio
ORIG_WHISPERX_DIR=$(BASE_DIR)/01.source_transcript_whisperX
TRIMMED_AUDIO_DIR=$(BASE_DIR)/02.source_audio_task2-3

# this target requires to be logged in on a machine with a GPU
# need to have the following pyenv activated: /lnet/troja/work/people/mnovak/virtualenvs/evaldio-python3.10-tdll8gpu4
# if "Killed", try changing asking for more memory by calling srun with --mem=50G
# or calling whisperX with float32 replaced by float16, or large-v2 by large-v1, medium, small etc.
$(ORIG_WHISPERX_DIR)/%.json : $(ORIG_AUDIO_DIR)/%.mp3
	mkdir -p $(dir $@)
	whisperx -o=$(dir $@) -f=json --language=cs --model=large-v2 --compute_type=float32 --diarize --hf_token=$(HF_TOKEN) $<

$(TRIMMED_AUDIO_DIR)/trim_start_times.tsv : $(ORIG_WHISPERX_DIR)/*.json
	mkdir -p $(dir $@)
	for f in $^; do \
		echo -en $$f"\t"; \
		jq '.' $$f | \
			grep -P -B2 '"text":.*bude.*[UuÚú]lo' | \
			grep start | \
			head -n1 | \
			sed 's/^.*: \(.*\),$$/\1/'; \
	done > $@ 

$(TRIMMED_AUDIO_DIR)/%.mp3 : $(ORIG_AUDIO_DIR)/%.mp3 $(TRIMMED_AUDIO_DIR)/trim_start_times.tsv
	mkdir -p $(dir $@)
	filename=`basename $(word 1,$^)`; \
	filebase=$${filename%.*}; \
	start_time=`cat $(word 2,$^) | grep "$$filebase" | cut -f2`; \
	ffmpeg -i $(word 1,$^) -vn -acodec copy -ss $$start_time $@
