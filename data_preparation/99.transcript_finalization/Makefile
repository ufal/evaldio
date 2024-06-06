SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/redmine_data/annotation/transcripts
TGT_BASEDIR=$(ROOT_DIR)/redmine_data/final/transcripts
DATA_TYPE=

ifeq ($(DATA_TYPE),manual)
SRC_DIR=$(SRC_BASEDIR)/04.manual
TGT_DIR=$(TGT_BASEDIR)/manual
else
SRC_DIR=$(SRC_BASEDIR)/01.auto
TGT_DIR=$(TGT_BASEDIR)/auto
endif

SRC_FILES=$(wildcard $(SRC_DIR)/*.xml)
TGT_FILES=$(SRC_FILES:$(SRC_DIR)/%.xml=$(TGT_DIR)/%.xml)

####### RECIPES #######

finalize_auto :
	$(MAKE) finalize DATA_TYPE=auto
finalize_manual :
	$(MAKE) finalize DATA_TYPE=manual

finalize : $(TGT_FILES) rename

$(TGT_DIR)/%.xml : $(SRC_DIR)/%.xml
	cat $< | \
		python3 normalize.py | \
		xmllint --format - > $@

rename :
	cd $(TGT_DIR); \
	for f in *.xml; do \
		bf=`basename $$f`; \
		newbf=`echo $$bf | sed 's/^\([A-Z]\+\)-\(.*\)-\(from_.*\.xml\)$$/\2-\1-\3/'`; \
		if [ "$$bf" != "$$newbf" ]; then \
			mv $$bf $$newbf; \
		fi; \
	done
