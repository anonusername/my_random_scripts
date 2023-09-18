#!/usr/bin/env fish

# Default option for SponsorBlock
set SPONSORBLOCK_OPTION "--sponsorblock-remove=all"

# Function to display usage instructions
function usage
    echo "Usage: $argv[0] <YouTube_URL> [OPTIONS]"
    echo "Options:"
    echo "  --no-sponsorblock    Exclude SponsorBlock removal"
    echo "  --help, -?            Show this help message"
end

# Check if yt-dlp is installed
if not command -q yt-dlp
    echo "yt-dlp is not installed. Please install it first."
    exit 1
end

# Check if FFmpeg is installed
if not command -q ffmpeg
    echo "FFmpeg is not installed. FFmpeg is required for SponsorBlock removal."
    exit 1
end

# Check for the optional arguments
if count $argv = 0
    usage
    exit 0
end

for arg in $argv
    switch $arg
        case "--no-sponsorblock"
            set SPONSORBLOCK_OPTION ""
        case "--help", "-?"
            usage
            exit 0
        case '*'
            set URL $arg
            break
    end
end

# Download video using yt-dlp with best format and auto-convert to MP4
yt-dlp -f 'best' --merge-output-format mp4 $SPONSORBLOCK_OPTION $URL

echo "Video downloaded and processed successfully."
