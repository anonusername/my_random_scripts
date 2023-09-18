# Default option for SponsorBlock
$SPONSORBLOCK_OPTION = "--sponsorblock-remove=all"

# Function to display usage instructions
function Show-Usage {
    Write-Host "Usage: $ScriptName <YouTube_URL> [OPTIONS]"
    Write-Host "Options:"
    Write-Host "  --no-sponsorblock    Exclude SponsorBlock removal"
    Write-Host "  --help, -?            Show this help message"
}

# Check if yt-dlp is installed
if (-not (Test-Path -Path "yt-dlp" -PathType Leaf)) {
    Write-Host "yt-dlp is not installed. Please install it first."
    exit 1
}

# Check if FFmpeg is installed
if (-not (Test-Path -Path "ffmpeg" -PathType Leaf)) {
    Write-Host "FFmpeg is not installed. FFmpeg is required for SponsorBlock removal."
    exit 1
}

# Check for the optional arguments
if ($args.Count -eq 0) {
    Show-Usage
    exit 0
}

$foundUrl = $false

foreach ($arg in $args) {
    switch ($arg) {
        "--no-sponsorblock" {
            $SPONSORBLOCK_OPTION = ""
        }
        "--help" {
            Show-Usage
            exit 0
        }
        "-?" {
            Show-Usage
            exit 0
        }
        default {
            if (-not $foundUrl) {
                $URL = $arg
                $foundUrl = $true
            } else {
                Show-Usage
                exit 1
            }
        }
    }
}

# Download video using yt-dlp with best format and auto-convert to MP4
Start-Process "yt-dlp" "-f 'best' --merge-output-format mp4 $SPONSORBLOCK_OPTION $URL" -Wait

Write-Host "Video downloaded and processed successfully."
