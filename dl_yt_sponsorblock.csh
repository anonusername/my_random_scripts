#!/bin/csh

# Default option for SponsorBlock
set SPONSORBLOCK_OPTION "--sponsorblock-remove=all"

# Function to display usage instructions
proc usage
    echo "Usage: $0 <YouTube_URL> [OPTIONS]"
    echo "Options:"
    echo "  --no-sponsorblock    Exclude SponsorBlock removal"
    echo "  --help, -?            Show this help message"
end

# Check if yt-dlp is installed
if ( ! which yt-dlp ) then
    echo "yt-dlp is not installed. Please install it first."
    exit 1
endif

# Check if FFmpeg is installed
if ( ! which ffmpeg ) then
    echo "FFmpeg is not installed. FFmpeg is required for SponsorBlock removal."
    exit 1
endif

# Check for the optional arguments
if ( $#argv == 0 ) then
    usage
    exit 0
endif

set found_url 0

foreach arg ( $argv:q )
    switch ( $arg )
        case "--no-sponsorblock":
            set SPONSORBLOCK_OPTION ""
            breaksw
        case "--help":
        case "-?":
            usage
            exit 0
            breaksw
        default:
            if ( $found_url == 0 ) then
                set URL $arg
                set found_url 1
            else
                usage
                exit 1
            endif
            breaksw
    endsw
end

# Download video using yt-dlp with best format and auto-convert to MP4
yt-dlp -f 'best' --merge-output-format mp4 $SPONSORBLOCK_OPTION $URL

echo "Video downloaded and processed successfully."
