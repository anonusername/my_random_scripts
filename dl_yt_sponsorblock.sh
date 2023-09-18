#!/bin/bash

# Default option for SponsorBlock
SPONSORBLOCK_OPTION="--sponsorblock-remove=all"

# Function to display usage instructions
usage() {
    echo "Usage: $0 <YouTube_URL> [OPTIONS]"
    echo "Options:"
    echo "  --no-sponsorblock    Exclude SponsorBlock removal"
    echo "  --help, -?            Show this help message"
}

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp is not installed. Please install it first."
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed. FFmpeg is required for SponsorBlock removal."
    exit 1
fi

# Check for the optional arguments
if [ $# -eq 0 ]; then
    usage
    exit 0
fi

while [ $# -gt 0 ]; do
    case "$1" in
        --no-sponsorblock)
            SPONSORBLOCK_OPTION=""
            ;;
        --help | -\?)
            usage
            exit 0
            ;;
        *)
            # Input URL
            URL="$1"
            break
            ;;
    esac
    shift
done

# Download video using yt-dlp with best format and auto-convert to MP4
yt-dlp -f 'best' --merge-output-format mp4 $SPONSORBLOCK_OPTION "$URL"

echo "Video downloaded and processed successfully."
