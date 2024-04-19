SHELL=/bin/bash

DATA_DIR=/lnet/ms/data/CoCzeFLA/exams/UJOP/CCE-A2_2024_01_26
SRC_DIR=$(DATA_DIR)/04.task2-3_mixed_transcripts
TGT_DIR=$(DATA_DIR)/05.task2-3_for_annotators

SRC_FILES=$(SRC_DIR)/A2ML_{220919,221205}_*.xml

SRC_PATTERN=\(.*\)_anonym_audio\.xml

SELECTION_RULE=$$((i+1))'~'$${#annotators[@]}
ANNOTATORS=MH ZM KV LR ET AP

all : distrib_2024-03-16 distrib_2024-04-19

distribute :
	mkdir -p $(TGT_DIR)
	ls $(SRC_FILES) | shuffle --random_seed 1986 > $(TGT_DIR)/shuffled_srcfiles.txt
	annotators=($(ANNOTATORS)); \
	for i in $${!annotators[@]}; do \
		cat $(TGT_DIR)/shuffled_srcfiles.txt | \
		sed -n $(SELECTION_RULE)'p' | \
		while read srcfile; do \
			basefile=`basename $$srcfile`; \
			tgtfile=$(TGT_DIR)/`echo $$basefile | \
				sed 's|$(SRC_PATTERN)|'$${annotators[$$i]}'-\1-__HASHCODE__.xml|'`; \
			hashcode=`echo "$$srcfile" | md5sum | cut -c1-10`; \
			tgtfile=`echo $$tgtfile | sed "s/__HASHCODE__/$$hashcode/"`; \
			ln -s $$srcfile $$tgtfile; \
			echo -e "$$tgtfile\t$$srcfile" >> $(TGT_DIR)/map_table.tsv; \
		done; \
	done
	rm $(TGT_DIR)/shuffled_srcfiles.txt

# the pilot distribution of recordings from UJOP
distrib_2024-03-16 :
	make distribute ANNOTATORS="MH ZM KV LR ET AP" SELECTION_RULE='$$$$((i+1))' TGT_DIR=$(TGT_DIR)/2024-03-16

# the second distribution of recordings from UJOP that we are allowed to publish
distrib_2024-04-19 :
	make distribute ANNOTATORS="MH" SELECTION_RULE='$$$$((i+1+6))' TGT_DIR=$(TGT_DIR)/2024-04-19
	make distribute ANNOTATORS="ZM KV LR ET AP" SELECTION_RULE='$$$$((i+1+7))' TGT_DIR=$(TGT_DIR)/2024-04-19
	make distribute ANNOTATORS="ZM KV LR ET AP" SELECTION_RULE='$$$$((i+1+12))' TGT_DIR=$(TGT_DIR)/2024-04-19

clean :
	rm -rf $(TGT_DIR)
