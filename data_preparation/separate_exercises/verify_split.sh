#!/bin/bash

audio_file=$1
times_file=$2
excerpt_half_length=$3
tgt_path=$4

(
read -e split_name
while read -e split_time; do
	start_time=`echo $split_time - $excerpt_half_length | bc`
	end_time=`echo $split_time + $excerpt_half_length | bc`
    excerpt_file="$tgt_path.$split_name.verify_split_excerpt.mp3"
    verify_file="$tgt_path.$split_name.verify_split.mp3"
    ffmpeg -nostdin -i $audio_file -ss $start_time -to $end_time -c copy "$excerpt_file"
	ffmpeg -nostdin -i $excerpt_file -i beep.mp3 -filter_complex \
		"[1:a]adelay="$excerpt_half_length"000|"$excerpt_half_length"000[b]; [0:a][b]amix=inputs=2" \
		-c:a libmp3lame -q:a 2 $verify_file
	rm $excerpt_file
    start_time=$end_time
    read -e split_name
done
) < $times_file
