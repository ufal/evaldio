#!/bin/bash

audio_file=$1
times_file=$2
tgt_dir=$3

(
start_time=0
read -e split_name
echo "[$split_name]"
while read -e end_time; do
    new_audio_file="$tgt_dir/"$(basename $audio_file .mp3)"-$split_name.mp3"
    echo "$new_audio_file"
    ffmpeg -nostdin -i $audio_file -ss $start_time -to $end_time -c copy "$new_audio_file"
    start_time=$end_time
    read -e split_name
    echo "[$split_name]"
done
new_audio_file="$tgt_dir/"$(basename $audio_file .mp3)"-$split_name.mp3"
echo "$new_audio_file"
ffmpeg -nostdin -i $audio_file -ss $start_time -c copy "$new_audio_file"
) < $times_file
