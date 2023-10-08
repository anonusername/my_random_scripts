import os
import argparse
from moviepy.editor import VideoFileClip
import shutil
import subprocess

# Short Video Finder and Looper
#
# This Python script searches for video files in a specified directory and its subdirectories.
# It identifies videos that have a duration of less than 30 seconds and offers the option to loop
# these short videos to exceed 30 seconds. The original short videos are moved to a "shorts"
# subdirectory, and the looped videos are saved in a "looped" subdirectory within the root directory.
#
# Usage:
# python make_loops_longer.py <root_directory>
#
# <root_directory>: The root directory where the script will start searching for video files.
#
# The script performs the following steps:
# 1. Counts the total number of media files that will be scanned.
# 2. Searches for video files (based on extensions) and identifies videos with a duration of less than 30 seconds.
# 3. Displays a progress meter during the scan.
# 4. Offers the choice to loop the short videos or not.
# 5. If chosen, it loops the videos to either exceed 30 seconds or loop a minimum of 3 times (whichever is longer).
# 6. Moves the original short videos to a "shorts" subdirectory in the root directory.
# 7. Saves the looped videos in a "looped" subdirectory in the root directory.
#
# Dependencies:
# - moviepy library for video duration checking
# - ffmpeg for video looping without re-encoding
#
# Note: Ensure that the moviepy library and ffmpeg are installed on your system.

def count_media_files(root_dir):
    total_files = 0

    for root, _, files in os.walk(root_dir):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Check if the file is a video based on its extension
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            if any(filepath.lower().endswith(ext) for ext in video_extensions):
                total_files += 1

    return total_files

def find_short_videos(root_dir, total_files):
    short_videos = []
    checked_files = 0

    for root, _, files in os.walk(root_dir):
        for filename in files:
            checked_files += 1
            filepath = os.path.join(root, filename)

            # Check if the file is a video based on its extension
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            if any(filepath.lower().endswith(ext) for ext in video_extensions):
                try:
                    # Load the video and get its duration
                    video = VideoFileClip(filepath)
                    duration = video.duration

                    # Check if the duration is less than 30 seconds
                    if duration < 30:
                        short_videos.append((filepath, duration))

                except Exception as e:
                    print(f"Error processing {filepath}: {str(e)}")

            # Update the progress timer
            print(f"Progress: {checked_files}/{total_files} media files checked", end="\r")

    return short_videos

def loop_videos(short_videos, root_dir):
    looped_dir = os.path.join(root_dir, "looped")
    if not os.path.exists(looped_dir):
        os.makedirs(looped_dir)

    for filepath, duration in short_videos:
        # Calculate the number of times to loop the video
        num_loops = max(3, int((30 / duration) + 1))

        # Define the output file path in the "looped" subdirectory
        output_path = os.path.join(looped_dir, os.path.basename(filepath))

        # Use FFmpeg to loop the video without re-encoding and show progress
        command = [
            'ffmpeg',
            '-y',  # Suppress overwrite prompt
            '-progress', 'pipe:1',  # Show progress
            '-stream_loop', str(num_loops),
            '-i', filepath,
            '-c', 'copy',
            output_path,
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def move_short_videos(short_videos, root_dir):
    shorts_dir = os.path.join(root_dir, "shorts")
    if not os.path.exists(shorts_dir):
        os.makedirs(shorts_dir)

    for filepath, _ in short_videos:
        # Define the destination file path in the "shorts" subdirectory
        destination_path = os.path.join(shorts_dir, os.path.basename(filepath))

        # Move the short video to the "shorts" subdirectory
        shutil.move(filepath, destination_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find videos less than 30 seconds in duration in a directory and loop them.")
    parser.add_argument("root_directory", help="Root directory to search for videos")

    args = parser.parse_args()
    
    total_files = count_media_files(args.root_directory)
    
    if total_files > 0:
        print(f"Total media files to scan: {total_files}")
        
        short_videos_list = find_short_videos(args.root_directory, total_files)
        
        if short_videos_list:
            print("\nVideos less than 30 seconds found:")
            for filepath, duration in short_videos_list:
                print(f"File: {filepath}, Duration: {duration} seconds")
            
            choice = input("Do you want to loop these videos? (Y/n): ").strip()
            if choice.lower() != "n":
                loop_videos(short_videos_list, args.root_directory)
                print("\nVideos have been looped and saved in the 'looped' directory inside the root directory.")
            
            move_short_videos(short_videos_list, args.root_directory)
            print("Short videos have been moved to the 'shorts' directory inside the root directory.")
        else:
            print("No videos less than 30 seconds found.")
    else:
        print("No media files found in the specified directory.")
