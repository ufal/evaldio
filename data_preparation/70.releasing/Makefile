SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/separate_exercises
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/70.releasing
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)

RELEASE_DIR=$(ROOT_DIR)/public_html-release

RELEASE_NAME=EvaldioData-1.0

FORMAT_SIMPLE_SCRIPT=../60.format_simple/format_simple.sh

CANONICAL=
ifeq ($(CANONICAL),1)
CANONICAL_FLAG=--canonical
endif

DATE=$(shell date +%Y%m%d)

############ RULES ################

release_A2_202410:
	$(MAKE) copy_audio copy_finalize_annot prepare zip deploy BATCH_PATH=release_A2_202410

runparser.pl :
	wget -O $@ https://gitlab.com/maartenes/TEITOK/-/raw/master/common/Scripts/runparser.pl?inline=false

copy_audio : $(BATCH_PATH).exer_numbers.csv
	mkdir -p $(TGT_DIR)
	while read fid exer; do \
		cp -v $(SRC_DIR)/$$fid*-$$exer.mp3 $(TGT_DIR); \
	done < $<

.PRECIOUS : $(TGT_DIR)/%.xml $(TGT_DIR)/%.xml.parsed $(TGT_DIR)/%.xml.tokenized

$(TGT_DIR)/%.txt : $(SRC_DIR)/%.xml
	$(FORMAT_SIMPLE_SCRIPT) < $< > $@

$(TGT_DIR)/%.xml : $(TGT_DIR)/%.xml.with_header
	xmllint --format - < $< > $@

$(TGT_DIR)/%.xml.with_header : $(TGT_DIR)/%.xml.parsed
	python add_proper_tei_header.py $(CANONICAL_FLAG) $< $@

$(TGT_DIR)/%.xml.parsed : $(TGT_DIR)/%.xml.tokenized
	cp $< $@
	sleep 1
	perl runparser.pl --verbose --model=ces --filename=$@ --killsent

$(TGT_DIR)/%.xml.tokenized : $(TGT_DIR)/%.xml.specstr_replaced
	cat $< | \
		python tokenize_before.py | \
		curl -s -F data=@- -F input=horizontal -F model=czech-pdt-ud-2.12-230717 -F tokenizer=presegmented -F tagger= -F parser= -F output=horizontal https://lindat.mff.cuni.cz/services/udpipe/api/process | \
		python tokenize_after.py $< > $@

$(TGT_DIR)/%.xml.specstr_replaced : $(SRC_DIR)/%.xml
	sed 's|xxx|<anon/>|g; s|\*\*\*|<gap reason="unintelligible"/>|g' < $< > $@

copy_finalize_annot : $(BATCH_PATH).exer_numbers.csv runparser.pl
	mkdir -p $(TGT_DIR)
	RANDOM=2024; \
	while read fid exer; do \
		annot_count=`ls $(SRC_DIR)/$$fid*-$$exer.xml | wc -l`; \
		rand_i=$$((RANDOM % $$annot_count)); \
		i=0; \
		for f in $(SRC_DIR)/$$fid*-$$exer.xml; do \
			if [ $$i -eq $$rand_i ]; then \
				canonical=1; \
			else \
				canonical=0; \
			fi; \
			bf=`basename $$f .xml`; \
			echo "===== $$f ====="; \
			make $(TGT_DIR)/$$bf.xml CANONICAL=$$canonical; \
			make $(TGT_DIR)/$$bf.txt; \
			i=$$((i+1)); \
		done; \
	done < $<

prepare : README.md LICENSE.txt
	mkdir -p $(TGT_DIR)/$(RELEASE_NAME)
	mkdir -p $(TGT_DIR)/$(RELEASE_NAME)/recordings
	mkdir -p $(TGT_DIR)/$(RELEASE_NAME)/annotations/teitok
	mkdir -p $(TGT_DIR)/$(RELEASE_NAME)/annotations/simple
	python copy_rename.py --verbose $(TGT_DIR)/*.mp3 $(TGT_DIR)/$(RELEASE_NAME)/recordings
	python copy_rename.py --verbose $(TGT_DIR)/*.xml $(TGT_DIR)/$(RELEASE_NAME)/annotations/teitok
	python copy_rename.py --verbose $(TGT_DIR)/*.txt $(TGT_DIR)/$(RELEASE_NAME)/annotations/simple
	cp -v $^ $(TGT_DIR)/$(RELEASE_NAME)

zip :
	cd $(TGT_DIR) && \
		zip -r $(RELEASE_NAME).zip $(RELEASE_NAME)

deploy :
	mkdir -p $(RELEASE_DIR)
	cp -v $(TGT_DIR)/$(RELEASE_NAME).zip $(RELEASE_DIR)/$(RELEASE_NAME)_v$(DATE).zip

clean_soft :
	rm -f $(TGT_DIR)/*.mp3
	rm -f $(TGT_DIR)/*.xml $(TGT_DIR)/*.xml.with_header
	rm -f $(TGT_DIR)/*.txt
	rm -f $(TGT_DIR).zip
	rm -f $(TGT_DIR)/$(RELEASE_NAME).zip
	rm -rf $(TGT_DIR)/$(RELEASE_NAME)

clean :
	rm -rf $(TGT_DIR)
	rm -f $(TGT_DIR).zip
