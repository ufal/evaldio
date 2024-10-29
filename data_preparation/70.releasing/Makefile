SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/separate_exercises
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/70.releasing
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)

RELEASE_DIR=~/public_html/evaldio/release

DATE=$(shell date +%Y%m%d)

############ RULES ################

release_A2_202410:
	$(MAKE) clean copy_audio copy_finalize_annot zip deploy BATCH_PATH=release_A2_202410

runparser.pl :
	wget -O $@ https://gitlab.com/maartenes/TEITOK/-/raw/master/common/Scripts/runparser.pl?inline=false

copy_audio : $(BATCH_PATH).exer_numbers.csv
	mkdir -p $(TGT_DIR)
	while read fid exer; do \
		cp -v $(SRC_DIR)/$$fid*-$$exer.mp3 $(TGT_DIR); \
	done < $<

.PRECIOUS : $(TGT_DIR)/%.xml $(TGT_DIR)/%.xml.parsed $(TGT_DIR)/%.xml.tokenized

$(TGT_DIR)/%.xml : $(TGT_DIR)/%.xml.with_header
	xmllint --format - < $< > $@

$(TGT_DIR)/%.xml.with_header : $(TGT_DIR)/%.xml.parsed
	python add_proper_tei_header.py $< $@

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
	while read fid exer; do \
		for f in $(SRC_DIR)/$$fid*-$$exer.xml; do \
			bf=`basename $$f`; \
			echo "===== $$f ====="; \
			make $(TGT_DIR)/$$bf; \
		done; \
	done < $<

zip :
	cd $(TGT_BASEDIR) && \
		zip -r $(BATCH_PATH).zip $(BATCH_PATH)

deploy :
	mkdir -p $(RELEASE_DIR)
	cp -v $(TGT_DIR).zip $(RELEASE_DIR)/`basename $(TGT_DIR).zip .zip`_v$(DATE).zip

clean_soft :
	rm -f $(TGT_DIR)/*.mp3
	rm -f $(TGT_DIR)/*.xml $(TGT_DIR)/*.xml.with_header
	rm -f $(TGT_DIR).zip

clean :
	rm -rf $(TGT_DIR)
	rm -f $(TGT_DIR).zip
