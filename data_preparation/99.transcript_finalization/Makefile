SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/redmine_data/annotation/transcripts
TGT_BASEDIR=$(ROOT_DIR)/redmine_data/final/transcripts
FOR_ANNOT_BASEDIR=../../../../tmp/data_preparation/*/*/05.task2-3_for_annotators/*/
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

finalize : clean $(TGT_FILES) uncover_source recname_first

$(TGT_DIR)/%.xml : $(SRC_DIR)/%.xml
	cat $< | \
		python3 normalize.py | \
		xmllint --format - > $@

uncover_source :
	cd $(TGT_DIR); \
	for f in *.xml; do \
		bf=`basename $$f`; \
		orig=`readlink $(FOR_ANNOT_BASEDIR)/$$bf`; \
		if [ -n "$$orig" ]; then \
			type=`if [[ $$orig == *'mixed'* ]]; then echo "mixed"; elif [[ $$orig == *'whisperX'* ]]; then echo "whisperX"; fi`; \
			bf_from=`echo $$bf | sed "s/-[^-]\+\.xml/-from_$$type.xml/"`; \
			mv $$bf $$bf_from; \
		fi; \
	done

recname_first :
	cd $(TGT_DIR); \
	for f in *.xml; do \
		bf=`basename $$f`; \
		newbf=`echo $$bf | sed 's/^\([A-Z]\+\)-\(.*\)-\(from_.*\.xml\)$$/\2-\1-\3/'`; \
		if [ "$$bf" != "$$newbf" ]; then \
			mv $$bf $$newbf; \
		fi; \
	done

clean :
	rm $(TGT_DIR)/*
