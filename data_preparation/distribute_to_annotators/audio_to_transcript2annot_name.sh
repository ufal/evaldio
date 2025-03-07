#!/bin/bash

src_f=$1
annotator=$2
transcripttype=$3
src_pattern='\(.*\)_anonym_.*\.xml'

if [ -z "$transcripttype" ]; then
    transcripttype=`echo "$src_f" | md5sum | cut -c1-10`
fi

src_bf=`basename $src_f`
echo $src_bf | sed "s|$src_pattern|$annotator-\1-$transcripttype.xml|"
