SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/data/exams/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation

BATCH=

####### PARAMS #######

PARAMS_UJOP/CCE-A1_2024_06_11 :=       LEVEL=A1        INPUT_CSV=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.A1.csv
PARAMS_UJOP/CCE-A2_2024_01_26 :=       LEVEL=A2        INPUT_CSV=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.A2.csv
PARAMS_UJOP/CCE-A2_2024_04_24 :=       LEVEL=A2        INPUT_CSV=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.A2.csv
PARAMS_UJOP/CCE-A2_older_2025_02_17 := LEVEL=A2_older  INPUT_CSV=$(SRC_BASEDIR)/UJOP/Hodnoceni_nahravek_starsi_kriteria_NAKI.csv


####### TARGETS #######

extract :
	make $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/done $(PARAMS_$(BATCH))

$(TGT_BASEDIR)/%/20.extract_labels/done : $(INPUT_CSV) $(SRC_BASEDIR)/%
	mkdir -p $(dir $@)
	python3 prepare_labels_old_exams.py --exam-type $(LEVEL) --audio-dir $(word 2,$^) $(word 1,$^) $(dir $@)
	touch $@

clean :
	rm -rf $(TGT_BASEDIR)/$(BATCH)/20.extract_labels