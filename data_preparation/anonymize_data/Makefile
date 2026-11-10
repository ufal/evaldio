SHELL=/bin/bash

####### DIR VARIABLES #######

ROOT_DIR=../..

SRC_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/separate_exercises
TGT_BASEDIR=$(ROOT_DIR)/tmp/data_preparation/anonymize_data
BATCH_PATH=

SRC_DIR=$(SRC_BASEDIR)/$(BATCH_PATH)
TGT_DIR=$(TGT_BASEDIR)/$(BATCH_PATH)


########### SPLIT OF RECORDINGS ############

$(TGT_DIR)/%.mp3 : $(SRC_DIR)/%.mp3 $(TGT_DIR)/%.anonymize_times.txt

