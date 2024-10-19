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
	$(MAKE) clean copy zip deploy BATCH_PATH=release_A2_202410

copy : $(BATCH_PATH).exer_numbers.csv
	mkdir -p $(TGT_DIR)
	while read fid exer; do \
		cp -v $(SRC_DIR)/$$fid*.$$exer.{mp3,xml} $(TGT_DIR); \
	done < $<

zip :
	cd $(TGT_BASEDIR) && \
		zip -r $(BATCH_PATH).zip $(BATCH_PATH)

deploy :
	mkdir -p $(RELEASE_DIR)
	cp -v $(TGT_DIR).zip $(RELEASE_DIR)/`basename $(TGT_DIR).zip .zip`_v$(DATE).zip

clean :
	rm -rf $(TGT_DIR)
	rm -f $(TGT_DIR).zip
