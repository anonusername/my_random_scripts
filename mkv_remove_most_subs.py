#!/bin/bash
# The reason this script was made was because a show came loaded with a million subtitles.
# Lots of subtitles is both annoying to work with but too many subtitles means Plex won't
# be able to play it on mobile or trancodes it.
#
# I set the script to only return English and Spanish and set the first English track as the default
#


# Check if the required tool 'mkvmerge' is installed
if ! command -v mkvmerge &> /dev/null; then
    echo "mkvmerge is not installed. Please install it before running this script."
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install it before running this script."
    exit 1
fi

# Iterate over all .mkv files in the current directory
for input_file in *.mkv; do
    if [ -e "$input_file" ]; then
        echo "Processing file: $input_file"

        # Extract the basename of the input file without extension
        input_basename="$(basename -- "$input_file")"
        input_basename_no_ext="${input_basename%.*}"

        # Run mkvmerge to identify the tracks and store the output in JSON format
        identify_output=$(mkvmerge --identification-format json --identify "$input_file")

        # Initialize an empty array to store matching subtitle track IDs
        matching_track_ids=()

        # Use jq to parse the JSON output and extract subtitle tracks with English or Spanish language
        while IFS= read -r track_info; do
            language=$(echo "$track_info" | jq -r '.properties.language')
            track_name=$(echo "$track_info" | jq -r '.properties.track_name')
            if [[ "$language" == "eng" || "$language" == "spa" ]] && ! [[ "$track_name" == *"European"* ]]; then
                track_id=$(echo "$track_info" | jq -r '.id')
                matching_track_ids+=("$track_id")
            fi
        done < <(echo "$identify_output" | jq -c '.tracks[] | select(.type == "subtitles")')

        # Check if there are any matching subtitle tracks
        if [ ${#matching_track_ids[@]} -eq 0 ]; then
            echo "No matching subtitle tracks found for English or Spanish in '$input_file'."
        else
            echo "Matching subtitle track IDs for English or Spanish (excluding 'European') in '$input_file':"
            for track_id in "${matching_track_ids[@]}"; do
                echo "$track_id"
            done

            # Create a comma-separated list of matching track IDs
            track_id_list=$(IFS=,; echo "${matching_track_ids[*]}")

            # Generate the output file name with " - desub" appended to the basename of the input file
            output_file="$input_basename_no_ext - desub.mkv"

            # Use mkvmerge to set the first "eng" subtitle track as default and save as the new output file
            default_track_id=$(echo "${matching_track_ids[0]}")
            mkvmerge --output "$output_file" --subtitle-tracks "$track_id_list" --default-track-flag "$default_track_id:yes" "$input_file"
            echo "Subtitles removed, and the first 'eng' subtitle track set as default. The result is saved as '$output_file'."
        fi
    fi
done
