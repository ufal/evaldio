SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/separate_exercises
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/anonymize_data
BATCH_PATH=release_B1_202610

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)
ANONYMIZE_TIMES_FILE=$(BATCH_PATH).anonymize_times.csv
AUDIO_FILES=$(shell awk -F '\t' '{print $$1}' $(ANONYMIZE_TIMES_FILE))
TGT_AUDIO_FILES=$(addprefix $(TGT_DIR)/,$(AUDIO_FILES))
SRC_TRANSCRIPT_FILES=$(wildcard $(SRC_DIR)/*.xml)
TGT_TRANSCRIPT_FILES=$(patsubst $(SRC_DIR)/%.xml,$(TGT_DIR)/%.xml,$(SRC_TRANSCRIPT_FILES))
ANONYMIZED_AUDIO_FILES=$(shell awk -F '\t' 'NF > 1 && $$2 != "" {print $$1}' $(ANONYMIZE_TIMES_FILE))
VERIFY_FILES=$(addsuffix .verify.mp3,$(addprefix $(TGT_DIR)/,$(basename $(ANONYMIZED_AUDIO_FILES))))
VERIFY_BEFORE=10
VERIFY_AFTER=2
VERIFY_SILENCE=1

.PHONY: all verify_anonymization
all: $(TGT_AUDIO_FILES) $(TGT_TRANSCRIPT_FILES)


########### ANONYMIZE AUDIO ############

$(TGT_DIR)/%.anonymize_times.txt: $(ANONYMIZE_TIMES_FILE)
	mkdir -p $(TGT_DIR)
	awk -F '\t' -v filename='$*.mp3' '$$1 == filename { print $$2 }' $< > $@

$(TGT_DIR)/%.mp3: $(SRC_DIR)/%.mp3 $(TGT_DIR)/%.anonymize_times.txt
	mkdir -p $(TGT_DIR)
	ranges=$$(cat $(word 2,$^)); \
	if [ -z "$$ranges" ]; then \
		ffmpeg -nostdin -y -i "$<" -map 0:a:0 -c:a copy "$@"; \
	else \
		expression=; \
		for range in $$ranges; do \
			start=$${range%-*}; \
			end=$${range#*-}; \
			if [ "$$start" = "$$range" ] || [ "$$end" = "$$range" ]; then \
				echo "Invalid anonymization timeframe: $$range" >&2; \
				exit 1; \
			fi; \
			if [ -n "$$expression" ]; then expression="$$expression+"; fi; \
			expression="$${expression}between(t,$$start,$$end)"; \
		done; \
		filter="[0:a]volume=enable='$${expression}':volume=0[muted];[1:a]volume=enable='$${expression}':volume=0.3,volume=enable='not($${expression})':volume=0[beep];[muted][beep]amix=inputs=2:duration=first:normalize=0[out]"; \
		ffmpeg -nostdin -y -i "$<" -f lavfi -i "sine=frequency=1000:sample_rate=44100" -filter_complex "$$filter" -map "[out]" -c:a libmp3lame -q:a 2 "$@"; \
	fi

########### COPY TRANSCRIPTS (THEY SHOULD BE ALREADY ANONYMIZED) ############

$(TGT_DIR)/%.xml: $(SRC_DIR)/%.xml
	mkdir -p $(TGT_DIR)
	cp "$<" "$@"


########### VERIFY AUDIO ANONYMIZATION ############

verify_anonymization: $(VERIFY_FILES)

$(TGT_DIR)/%.verify.mp3: $(TGT_DIR)/%.mp3 $(TGT_DIR)/%.anonymize_times.txt verify_anonymization.sh
	mkdir -p $(TGT_DIR)
	./verify_anonymization.sh "$<" "$(TGT_DIR)/$*.anonymize_times.txt" "$@" $(VERIFY_BEFORE) $(VERIFY_AFTER) $(VERIFY_SILENCE)
