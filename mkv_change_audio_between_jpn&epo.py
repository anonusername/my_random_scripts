# Japanese to Esperanto Plex Hack
# When Plex parses an anime library ,which you set to only play Japanese audio, it will play Japanese audio with English subtitles.
# This is cool for 99% of all anime... except shows like Cowboy Bebop where the English audio dub is done with quality 
# hell, the creator said the English voice is Spike is very awesome 
# 
# This code will 
# *search a directory for "mkv" files, 
# *uses "mkvinfo" to pull all the information of the audio tracks from the mkv file
# *builds a "mkvpropedit" command to change all Japanese (jpn) audio tracks of that specific mkv file to Esperanto (code: epo)
# *if Esperanto audio is found, then it will switch it to Japanese (reversing my change)
# *prints out the mkvpropedit command
# *goes to next mkv file
# 
# I decided not to have the script do it automatically because I don't want it to fail in the middle of the process and leave with some changed files and some not. 
import subprocess
import re
import os
import sys

def extract_tracks_and_language_codes(mkv_file):
    output = subprocess.check_output(["mkvinfo", mkv_file], text=True)
    tracks_info = []
    track_out = []
    # Split the "mkvinfo" output into lines
    lines = output.split('\n')

    # Initialize variables to store extracted information

    track_number = None
    track_tool_id = None
    track_type = None
    language = None
    uuid = None

# Loop through each line and extract the desired information for audio and video tracks
    for line in lines:
        if "Track number:" in line:
            track_number = line.split(":")[1].strip().split()[0]
            if "track ID for mkvmerge & mkvextract:" in line:
                track_tool_id = re.search(r"mkvmerge & mkvextract: (\d+)", line ).group(1)
        elif "Track type:" in line:
            track_type = line.split(":")[1].strip()
        elif "Language:" in line:
            language = line.split(":")[1].strip()
        elif "Track UID:" in line:
            uuid = line.split(":")[1].strip()
        
        # Check if all the desired information has been extracted for a track
        
        if track_number is not None and track_tool_id is not None and track_type is not None and language is not None and uuid is not None:
        #if track_number is not None and track_tool_id is not None and track_type is not None and start_track == 1:
            # Filter for audio and video tracks only
            if track_type == 'audio' or track_type == 'video':
                track_out.append((track_number, track_tool_id, track_type, language,uuid))
                # Reset the variables for the next track
                track_number = None
                track_tool_id = None
                track_type = None
                language = None
                uuid = None
                
    return track_out

def build_mkvpropedit_line(mkvbasename: str,all_track_info: list):
    #example of switching audio language
    #--edit track:a1 --set language=fre --edit track:a2 --set language=ita
    
    command_out = "mkvpropedit " + mkvbasename + " "
    for track_info in all_track_info:
        track_number, track_tool_id, track_type, language,uuid = track_info
        if track_type == "audio":
            if language == "jpn":
                command_out = command_out + "--edit track:=" + uuid + " --set language=epo "
            elif language == "epo":
                command_out = command_out + "--edit track:=" + uuid + " --set language=jpn "
        
    return command_out

if len(sys.argv) != 2:
    print("Usage: python script.py <directory_path>")
    sys.exit(1)

# Get the directory path from command line argument
directory_path = sys.argv[1]
cwd = os.getcwd()
# Check if the provided directory path is valid
if not os.path.isdir(directory_path):
    print("Error: Invalid directory path")
    sys.exit(1)

# Use the directory_path variable as needed in your code
print("Directory path provided:", directory_path)

filepaths = []

files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
for filename in files:
    filepaths.append(os.path.normpath(os.path.join(cwd,directory_path, filename)))



mkv_filepaths = [fp for fp in filepaths if os.path.splitext(fp)[1] == '.mkv']

commands = []
for mkvfilepath in mkv_filepaths:
    command_mkvfilepath = mkvfilepath.replace(' ', r'\ ').replace('"', r'\"')..replace('(', '\\(').replace(')', '\\)')
    all_track_info = extract_tracks_and_language_codes(mkvfilepath)
    for track_info in all_track_info:
        track_number, track_tool_id, track_type, language,uuid = track_info
        #print(f"Track number: {track_number}, Track ID for mkvmerge & mkvextract: {track_tool_id}, Track type: {track_type}, Language: {language}, UUID: {uuid}")
    command = build_mkvpropedit_line(command_mkvfilepath,all_track_info)
    commands.append(build_mkvpropedit_line(command_mkvfilepath,all_track_info))



for command in commands:
    print(command)
