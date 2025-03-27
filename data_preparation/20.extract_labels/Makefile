SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/data/exams/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation

####### TARGETS #######

all : $(TGT_BASEDIR)/UJOP/CCE-A2_older_2025_02_17/20.extract_labels/done

$(TGT_BASEDIR)/UJOP/CCE-A2_older_2025_02_17/20.extract_labels/done : $(SRC_BASEDIR)/UJOP/Hodnoceni_nahravek_starsi_kriteria_NAKI.csv
	mkdir -p $(dir $@)
	python3 prepare_labels_old_exams.py $< $(dir $@)
	touch $@

clean :
	rm -rf $(TGT_BASEDIR)/UJOP/CCE-A2_older_2025_02_17/20.extract_labels