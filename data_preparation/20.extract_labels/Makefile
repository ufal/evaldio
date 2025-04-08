SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/data/exams/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation

BATCH=

####### PARAMS #######

PARAMS_UJOP/CCE-A1_2024_06_11 :=       LEVEL=A1        INPUT_XLSX=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx
PARAMS_UJOP/CCE-A2_2024_01_26 :=       LEVEL=A2        INPUT_XLSX=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx
PARAMS_UJOP/CCE-A2_2024_04_24 :=       LEVEL=A2        INPUT_XLSX=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx
PARAMS_UJOP/CCE-A2_older_2025_02_17 := LEVEL=A2_older  INPUT_XLSX=$(SRC_BASEDIR)/UJOP/Hodnoceni_nahravek_starsi_kriteria_NAKI.xlsx
PARAMS_UJOP/CCE-B1_2024_05_21 :=       LEVEL=B1        INPUT_XLSX=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx
PARAMS_UJOP/CCE-B2_2024_09_23 :=       LEVEL=B2        INPUT_XLSX=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx


####### TARGETS #######

all : jsons

.SECONDARY: $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/level.csv $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/overall.csv

########## CONVERTING XLSX TO CSV ##########

csv :
	$(MAKE) $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/level.csv $(PARAMS_$(BATCH))

overall :
	$(MAKE) $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/overall.csv $(PARAMS_$(BATCH))

$(TGT_BASEDIR)/UJOP/CCE-A2_older_2025_02_17/20.extract_labels/level.csv : $(SRC_BASEDIR)/UJOP/Hodnoceni_nahravek_starsi_kriteria_NAKI.xlsx
	mkdir -p $(dir $@)
	python3 xlsx_to_csv.py --sheet "A2 starší" $< $@

$(TGT_BASEDIR)/%/20.extract_labels/fixed.xlsx : $(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx
	@echo "Delete the autoFilter elements from the Excel file before running this script. The openpyxl library in the recent 3.1 version does not support them."
	mkdir -p $(dir $@)
	unzip $< -d $(dir $@)/xlsx_unzip
	for f in $(dir $@)/xlsx_unzip/xl/worksheets/sheet*.xml; do \
		mv $$f $$f.old; \
		python3 delete_autoFilter.py $$f.old $$f; \
		rm $$f.old; \
	done
	cd $(dir $@)/xlsx_unzip && \
		zip -r ../$(notdir $@) *
	rm -rf $(dir $@)/xlsx_unzip

$(TGT_BASEDIR)/%/20.extract_labels/level.csv : $(TGT_BASEDIR)/%/20.extract_labels/fixed.xlsx
	python3 xlsx_to_csv.py --sheet $(LEVEL) $< $@
	if [ -f data_patches/$(LEVEL).patch ]; then \
		patch $@ data_patches/$(LEVEL).patch; \
	fi

$(TGT_BASEDIR)/%/20.extract_labels/overall.csv : $(TGT_BASEDIR)/%/20.extract_labels/fixed.xlsx
	python3 xlsx_to_csv.py --sheet seznam_ukazek $< $@

############# EXTRACTING LABELS TO JSON FILES ############

jsons :
	$(MAKE) $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/done $(PARAMS_$(BATCH))

$(TGT_BASEDIR)/UJOP/CCE-A2_older_2025_02_17/20.extract_labels/done : $(TGT_BASEDIR)/UJOP/CCE-A2_older_2025_02_17/20.extract_labels/level.csv $(SRC_BASEDIR)/UJOP/CCE-A2_older_2025_02_17
	mkdir -p $(dir $@)
	python3 prepare_labels_old_exams.py --exam-type $(LEVEL) --audio-dir $(word 2,$^) $(word 1,$^) $(dir $@)
	touch $@

$(TGT_BASEDIR)/%/20.extract_labels/done : $(TGT_BASEDIR)/%/20.extract_labels/level.csv $(TGT_BASEDIR)/%/20.extract_labels/overall.csv $(SRC_BASEDIR)/%
	mkdir -p $(dir $@)
	python3 prepare_labels_old_exams.py --exam-type $(LEVEL) --audio-dir $(word 3,$^) --overall-csv $(word 2,$^) $(word 1,$^) $(dir $@)
	touch $@

########## CLEANING UP ##########

clean :
	rm -rf $(TGT_BASEDIR)/$(BATCH)/20.extract_labels

