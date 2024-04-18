SHELL=/bin/bash

SRC_DIR=
TGT_DIR=

$(TGT_DIR)/%.xml : $(SRC_DIR)/%.xml
	cat $< | \
	python scripts/normalize.py | \
	xmllint --format - > $@
