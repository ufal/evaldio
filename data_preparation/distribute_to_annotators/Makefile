SHELL=/bin/bash

#DATA_DIR=/lnet/ms/data/CoCzeFLA/exams/UJOP/CCE-A2_2024_01_26
SRC_DIR=04.task2-3_mixed_transcripts
TGT_DIR=05.task2-3_for_annotators
SRC_FILES=*.xml

SRC_FILES_PATH=$(DATA_DIR)/$(SRC_DIR)/$(SRC_FILES)
TGT_DIR_PATH=$(DATA_DIR)/$(TGT_DIR)

SRC_PATTERN=\(.*\)_anonym_audio\.xml

#SELECTION_RULE=$$((i+1))'~'$${#annotators[@]}
#ANNOTATORS=MH ZM KV LR ET AP

all : distrib_UJOP-CCE-A2-20240126

distrib_UJOP-CCE-A2-20240126 : distrib_2024-03-16 distrib_2024-04-19 distrib_2024-05-02

# the pilot distribution of recordings from UJOP
distrib_2024-03-16 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_\{220919,221205\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-03-16 \
		ANNOTATORS="MH ZM KV LR ET AP" \
		SELECTION_RULE='$$$$((i+1))'

# the second distribution of recordings from UJOP that we are allowed to publish
distrib_2024-04-19 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{220919,221205\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-04-19 \
		ANNOTATORS="MH" \
		SELECTION_RULE='$$$$((i+1+6))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{220919,221205\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-04-19 \
		ANNOTATORS="ZM KV LR ET AP" \
		SELECTION_RULE='$$$$((i+1+7))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{220919,221205\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-04-19 \
		ANNOTATORS="ZM KV LR ET AP" \
		SELECTION_RULE='$$$$((i+1+12))'

# the third distribution of recordings from UJOP that we are allowed to publish
distrib_2024-05-02 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{220919,221205\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-02 \
		ANNOTATORS="ET KV ZM" \
		SELECTION_RULE='$$$$((i+1+17))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_\{220919,221205\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-02 \
		ANNOTATORS="ET KV ZM" \
		SELECTION_RULE='$$$$((i+1+18))'
	# selecting from A2ML_{230724,230911}_*.json
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-02 \
		ANNOTATORS="KV ZM ET" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-02 \
		ANNOTATORS="ET KV ZM" \
		SELECTION_RULE='$$$$((i+1+1))'

distrib_2024-05-22 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-22 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+4))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-22 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+9))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-05-22 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+14))'

distrib_2024-06-03 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-03 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+19))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-03 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+20))'

distrib_2024-06-05 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-05 \
		ANNOTATORS="ET" \
		SELECTION_RULE='$$$$((i+1+21))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_\{230724,230911\}_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-05 \
		ANNOTATORS="ZM" \
		SELECTION_RULE='$$$$((i+1+22))'

distribute :
	mkdir -p $(TGT_DIR_PATH)
	ls $(SRC_FILES_PATH) | shuffle --random_seed 1986 > $(TGT_DIR_PATH)/shuffled_srcfiles.txt
	annotators=($(ANNOTATORS)); \
	for i in $${!annotators[@]}; do \
		cat $(TGT_DIR_PATH)/shuffled_srcfiles.txt | \
		sed -n $(SELECTION_RULE)'p' | \
		while read srcfile; do \
			basefile=`basename $$srcfile`; \
			tgtfile=$(TGT_DIR_PATH)/`echo $$basefile | \
				sed 's|$(SRC_PATTERN)|'$${annotators[$$i]}'-\1-__HASHCODE__.xml|'`; \
			hashcode=`echo "$$srcfile" | md5sum | cut -c1-10`; \
			tgtfile=`echo $$tgtfile | sed "s/__HASHCODE__/$$hashcode/"`; \
			ln -s $$srcfile $$tgtfile; \
			echo -e "$$tgtfile\t$$srcfile" >> $(TGT_DIR_PATH)/map_table.tsv; \
		done; \
	done
	rm $(TGT_DIR_PATH)/shuffled_srcfiles.txt

clean :
	rm -rf $(TGT_DIR_PATH)
