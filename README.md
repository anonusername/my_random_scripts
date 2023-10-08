# Media Toolkit

This repository contains a collection of Python scripts for performing various media-related tasks. Whether you need to download videos from popular services, convert media files, or perform specific actions on your media content, these scripts can help you automate these processes.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Scripts](#scripts)
   - [Video Downloader](#video-downloader)
   - [Media Converter](#media-converter)
   - [Short Video Finder and Looper](#short-video-finder-and-looper)
   - [Your Custom Script](#your-custom-script)
3. [Dependencies](#dependencies)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Getting Started

To use these scripts, you'll need Python installed on your system. Additionally, some scripts may have specific dependencies, which will be listed in the respective sections below.

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/media-toolkit.git
cd media-toolkit


## YouTube Video Downloader with SponsorBlock Removal

This Bash script simplifies the process of downloading YouTube videos using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and optionally removing SponsorBlock segments. It's a versatile tool for efficiently fetching and processing YouTube content.

Several versions of scripts exist; bash, fish, bourne, and powershell

### Usage:

To use this script, follow the provided usage instructions:

```
Usage: ./youtube_downloader.sh <YouTube_URL> [OPTIONS]

Options:
  --no-sponsorblock    Exclude SponsorBlock removal
  --help, -?            Show this help message
```

### Prerequisites:

- **yt-dlp:** Ensure that yt-dlp is installed on your system. If not, please install it before using this script.
- **FFmpeg:** FFmpeg is required for SponsorBlock removal, so make sure it's installed as well.

### How to Use:

1. Run the script with a YouTube video URL as an argument. For example:

   ```
   ./youtube_downloader.sh https://www.youtube.com/watch?v=your_video_id
   ```

2. By default, SponsorBlock segments will be removed. To exclude SponsorBlock removal, use the `--no-sponsorblock` option:

   ```
   ./youtube_downloader.sh https://www.youtube.com/watch?v=your_video_id --no-sponsorblock
   ```

3. If you ever need a reminder of how to use the script, just run it with the `--help` or `-?` option:

   ```
   ./youtube_downloader.sh --help
   ```

### What It Does:

- The script uses yt-dlp to download the YouTube video in the best available format.
- If the `--no-sponsorblock` option is used, SponsorBlock removal is skipped; otherwise, SponsorBlock segments are removed from the downloaded video.
- The resulting video is saved in MP4 format.

That's it! Enjoy downloading and processing YouTube videos with ease using this script.

---

Feel free to customize this description as needed for your documentation or README file.
