#!/bin/bash

# Check if the required tool 'mkvmerge' is installed
if ! command -v mkvmerge &> /dev/null; then
    echo "mkvmerge is not installed. Please install it before running this script."
    exit 1
fi

# Check if an input MKV file argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input.mkv>"
    exit 1
fi

# Get the input MKV file from the command line argument
input_file="$1"

# Run mkvmerge to identify the tracks and store the output in JSON format
identify_output=$(mkvmerge --identification-format json --identify "$input_file")

# Initialize an empty array to store matching subtitle track IDs
matching_track_ids=()

# Use jq to parse the JSON output and extract subtitle tracks with English or Spanish language
while IFS= read -r track_info; do
    language=$(echo "$track_info" | jq -r '.properties.language')
    if [[ "$language" == "eng" || "$language" == "spa" ]]; then
        track_id=$(echo "$track_info" | jq -r '.id')
        matching_track_ids+=("$track_id")
    fi
done < <(echo "$identify_output" | jq -c '.tracks[] | select(.type == "subtitles")')

# Check if there are any matching subtitle tracks
if [ ${#matching_track_ids[@]} -eq 0 ]; then
    echo "No matching subtitle tracks found for English or Spanish in '$input_file'."
else
    echo "Matching subtitle track IDs for English or Spanish in '$input_file':"
    for track_id in "${matching_track_ids[@]}"; do
        echo "$track_id"
    done
fi
