SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/redmine_data/annotation/transcripts
TGT_BASEDIR=$(ROOT_DIR)/redmine_data/final/transcripts
FOR_ANNOT_BASEDIR=../../../../tmp/data_preparation/*/*/05.task2-3_for_annotators/*
MIXED_BASEDIR=../../tmp/data_preparation/*/*/04.task2-3_mixed_transcripts
DATA_TYPE=

ifeq ($(DATA_TYPE),manual)
SRC_DIR=$(SRC_BASEDIR)/04.manual
TGT_DIR=$(TGT_BASEDIR)/manual
else ifeq ($(DATA_TYPE),before_review)
SRC_DIR=$(SRC_BASEDIR)/03.under_review
TGT_DIR=$(TGT_BASEDIR)/before_review
else
SRC_DIR=$(SRC_BASEDIR)/01.auto
TGT_DIR=$(TGT_BASEDIR)/auto
endif

SRC_FILES=$(wildcard $(SRC_DIR)/*.xml)
TGT_FILES=$(SRC_FILES:$(SRC_DIR)/%.xml=$(TGT_DIR)/%.xml)

####### RECIPES #######

finalize_auto :
	$(MAKE) finalize DATA_TYPE=auto
	$(MAKE) add_source_systems DATA_TYPE=auto
finalize_before_review :
	$(MAKE) finalize DATA_TYPE=before_review
	$(MAKE) add_annotation_durations DATA_TYPE=before_review
finalize_manual :
	$(MAKE) finalize DATA_TYPE=manual

finalize : $(TGT_FILES) uncover_source recname_first

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

add_source_systems :
	for f in $(TGT_DIR)/*-from_mixed.xml; do \
		bf=`basename $$f`; \
		fid=`echo $$bf | cut -f1 -d-`; \
		python3 add_sources_to_mixed.py $(MIXED_BASEDIR)/$$fid*.log < $$f > $$f.with_sources; \
		rm $$f; \
		mv $$f.with_sources $$f; \
	done

USERFILE_PATH=users.xml
ACTION_LOG_PATH=$(SRC_BASEDIR)/action.log

add_annotation_durations :
	# ignore the transcripts presumably already in progress
	cat $(ACTION_LOG_PATH) | \
		tail -n+11 | \
		python3 add_annotation_times.py --author-only --userfile $(USERFILE_PATH) $(TGT_DIR)/*.xml
	for f in $(TGT_DIR)/*.xml; do \
		xmllint --format $$f > $$f.pp; \
		mv $$f.pp $$f; \
	done

clean :
	rm $(TGT_DIR)/*
