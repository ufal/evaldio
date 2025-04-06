SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/data/exams/src_audio
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation

BATCH=

####### PARAMS #######

PARAMS_UJOP/CCE-A1_2024_06_11 :=       LEVEL=A1        INPUT_XLSX=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.xlsx
PARAMS_UJOP/CCE-A2_2024_01_26 :=       LEVEL=A2        INPUT_CSV=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.A2.csv
PARAMS_UJOP/CCE-A2_2024_04_24 :=       LEVEL=A2        INPUT_CSV=$(SRC_BASEDIR)/UJOP/UJOP_hodnoceni_nahravek_12_2_2025.A2.csv
PARAMS_UJOP/CCE-A2_older_2025_02_17 := LEVEL=A2_older  INPUT_CSV=$(SRC_BASEDIR)/UJOP/Hodnoceni_nahravek_starsi_kriteria_NAKI.csv


####### TARGETS #######

extract :
	make $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/done $(PARAMS_$(BATCH))

csv :
	make $(TGT_BASEDIR)/$(BATCH)/20.extract_labels/level.csv $(PARAMS_$(BATCH))

$(TGT_BASEDIR)/%/20.extract_labels/fixed.xlsx : $(INPUT_XLSX)
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

$(TGT_BASEDIR)/%/20.extract_labels/done : $(TGT_BASEDIR)/%/20.extract_labels/$(LEVEL).csv $(SRC_BASEDIR)/%
	mkdir -p $(dir $@)
	python3 prepare_labels_old_exams.py --exam-type $(LEVEL) --audio-dir $(word 2,$^) $(word 1,$^) $(dir $@)
	touch $@

clean :
	rm -rf $(TGT_BASEDIR)/$(BATCH)/20.extract_labels

.SECONDARY: $(TGT_BASEDIR)/%/20.extract_labels/$(LEVEL).csv