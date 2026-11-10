#!/bin/bash

set -euo pipefail

audio_file=$1
times_file=$2
output_file=$3
before=${4:-10}
after=${5:-2}
silence=${6:-1}

intervals_file=$(mktemp)
merged_file=$(mktemp)
trap 'rm -f "$intervals_file" "$merged_file"' EXIT

awk -v before="$before" -v after="$after" '
BEGIN {
	if (before !~ /^[0-9]+([.][0-9]+)?$/ || after !~ /^[0-9]+([.][0-9]+)?$/) {
		print "Excerpt padding must be non-negative numbers" > "/dev/stderr"
		exit 1
	}
}
{
	for (i = 1; i <= NF; i++) {
		if ($i !~ /^[0-9]+([.][0-9]+)?-[0-9]+([.][0-9]+)?$/) {
			print "Invalid anonymization timeframe: " $i > "/dev/stderr"
			exit 1
		}
		split($i, range, "-")
		start = range[1] + 0
		end = range[2] + 0
		if (end <= start) {
			print "Anonymization timeframe end must be after its start: " $i > "/dev/stderr"
			exit 1
		}
		start -= before
		if (start < 0) start = 0
		end += after
		printf "%.6f %.6f\n", start, end
	}
}' "$times_file" | sort -n -k1,1 > "$intervals_file"

awk '
NR == 1 {
	start = $1
	end = $2
	next
}
$1 <= end {
	if ($2 > end) end = $2
	next
}
{
	printf "%.6f %.6f\n", start, end
	start = $1
	end = $2
}
END {
	if (NR > 0) printf "%.6f %.6f\n", start, end
}' "$intervals_file" > "$merged_file"

if [ ! -s "$merged_file" ]; then
	echo "No anonymization timeframes found in $times_file" >&2
	exit 1
fi

if ! awk -v silence="$silence" 'BEGIN { exit !(silence ~ /^[0-9]+([.][0-9]+)?$/) }'; then
	echo "Silence duration must be a non-negative number" >&2
	exit 1
fi

mkdir -p "$(dirname "$output_file")"
filter=
labels=()
index=0
while read -r start end; do
	if [ "$index" -gt 0 ]; then
		filter+="anullsrc=r=44100:cl=stereo:d=${silence}[silence${index}];"
		labels+=("[silence$index]")
	fi
	filter+="[0:a]atrim=start=$start:end=$end,asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo[excerpt$index];"
	labels+=("[excerpt$index]")
	index=$((index + 1))
done < "$merged_file"

label_list=$(printf '%s' "${labels[@]}")
filter+="${label_list}concat=n=${#labels[@]}:v=0:a=1[out]"
ffmpeg -nostdin -y -i "$audio_file" -filter_complex "$filter" -map "[out]" -c:a libmp3lame -q:a 2 "$output_file"
