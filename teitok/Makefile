SHELL=/bin/bash

ANNOTATORS=MH ZM KV LR ET AP

prepare_for_teitok_transcribing:
	annotators=($(ANNOTATORS)); \
	for i in $${!annotators[@]}; do \
		ls output/A2ML_{220919,221205}_* | \
		shuffle --random_seed 1986 | \
		sed -n $$((i+1))'p' | \
		while read source; do \
			target=`echo $$source | \
				sed 's|output/\(.*\)_anonym_audio\.xml|before_postediting/'$${annotators[$$i]}'-from_whisperX-\1.xml|'`; \
			ln -s ../$$source $$target; \
		done; \
	done
