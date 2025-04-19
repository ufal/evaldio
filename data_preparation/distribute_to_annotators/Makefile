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

distrib_2024-06-07 :
	echo "TODO"

distrib_2024-06-14 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_221205_10_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-14 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_220919_02_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-14 \
		ANNOTATORS="ET" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_230724_29_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-14 \
		ANNOTATORS="KV" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_221205_04_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-14 \
		ANNOTATORS="KV" \
		SELECTION_RULE='$$$$((i+1))'

distrib_2024-06-18 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_02_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-18 \
		ANNOTATORS="ZM" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_11_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-18 \
		ANNOTATORS="ZM" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_07_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-18 \
		ANNOTATORS="ET" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.task2-3_trimmed_transcript/whisperX-large-v2 \
		SRC_FILES=A2ML_221205_01_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-18 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_18_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-06-18 \
		ANNOTATORS="LR" \
		SELECTION_RULE='$$$$((i+1))'

distrib_2024-07-04 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_06_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-07-04 \
		ANNOTATORS="ET" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_07_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-07-04 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1))'
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=04.task2-3_mixed_transcripts \
		SRC_FILES=A2ML_221205_16_*.xml \
		TGT_DIR=05.task2-3_for_annotators/2024-07-04 \
		ANNOTATORS="ZM" \
		SELECTION_RULE='$$$$((i+1))'

distrib_2024-08-31 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-08-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-08-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+5))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-08-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+10))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2024-09-06 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-09-06 \
		ANNOTATORS="ET LR ZM" \
		SELECTION_RULE='$$$$((i+1+15))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-09-06 \
		ANNOTATORS="ET LR ZM" \
		SELECTION_RULE='$$$$((i+1+18))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-09-06 \
		ANNOTATORS="ET LR ZM" \
		SELECTION_RULE='$$$$((i+1+21))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2024-10-04 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-10-04 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+24))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-10-04 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+29))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-10-04 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+34))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_01_26 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_\{220919,221205,230724,230911\}_??_01_*.xml \
		TGT_DIR=05.for_annotators/2024-10-04 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+39))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2025-01-31 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-01-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-01-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+5))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-01-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+10))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-01-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+15))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-01-31 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+20))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2025-03-07 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-03-07 \
		ANNOTATORS="AP ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+25))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-03-07 \
		ANNOTATORS="ET KV LR ZM" \
		SELECTION_RULE='$$$$((i+1+30))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-03-07 \
		ANNOTATORS="ET KV ZM" \
		SELECTION_RULE='$$$$((i+1+34))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-03-07 \
		ANNOTATORS="ET KV ZM" \
		SELECTION_RULE='$$$$((i+1+37))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-B1_2024_05_21 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=B1ML_23*.xml \
		TGT_DIR=05.for_annotators/2025-03-07 \
		ANNOTATORS="ET KV ZM" \
		SELECTION_RULE='$$$$((i+1+40))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2025-03-28 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_04_24 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_240221_81_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="KV" \
		SELECTION_RULE='$$$$((i+1))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_04_24 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_240221_83_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ZM" \
		SELECTION_RULE='$$$$((i+1))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A2_2024_04_24 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A2ML_240221_84_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ZM" \
		SELECTION_RULE='$$$$((i+1))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+2))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+4))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+6))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-03-28 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+8))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2025-04-11 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-11 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+10))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-11 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+11))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-11 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+12))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-11 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+13))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-11 \
		ANNOTATORS="AP" \
		SELECTION_RULE='$$$$((i+1+14))' \
		TRANSCRIPT_TYPE=from_scratch

distrib_2025-04-19 :
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-19 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+15))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-19 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+17))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-19 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+19))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-19 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+21))' \
		TRANSCRIPT_TYPE=from_scratch
	make distribute \
		DATA_DIR=/lnet/work/projects/evaldio/tmp/data_preparation/UJOP/CCE-A1_2024_06_11 \
		SRC_DIR=03.auto_transcripts/null \
		SRC_FILES=A1ML_*.xml \
		TGT_DIR=05.for_annotators/2025-04-19 \
		ANNOTATORS="ET LR" \
		SELECTION_RULE='$$$$((i+1+23))' \
		TRANSCRIPT_TYPE=from_scratch

distribute_manual :
	mkdir -p $(TGT_DIR_PATH)

distribute :
	mkdir -p $(TGT_DIR_PATH)
	ls $(SRC_FILES_PATH) | shuffle --random_seed 1986 > $(TGT_DIR_PATH)/shuffled_srcfiles.txt
	annotators=($(ANNOTATORS)); \
	for i in $${!annotators[@]}; do \
		cat $(TGT_DIR_PATH)/shuffled_srcfiles.txt | \
		sed -n $(SELECTION_RULE)'p' | \
		while read srcfile; do \
			tgt_bf=`./audio_to_transcript2annot_name.sh $$srcfile $${annotators[$$i]} $(TRANSCRIPT_TYPE)`; \
			tgtfile=$(TGT_DIR_PATH)/$$tgt_bf; \
			ln -s $$srcfile $$tgtfile; \
			echo -e "$$tgtfile\t$$srcfile" >> $(TGT_DIR_PATH)/map_table.tsv; \
		done; \
	done
	rm $(TGT_DIR_PATH)/shuffled_srcfiles.txt

clean :
	rm -rf $(TGT_DIR_PATH)
