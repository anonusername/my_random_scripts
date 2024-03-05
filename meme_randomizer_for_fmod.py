import os
import subprocess
import shutil
import random

# Create a function to copy .wav and .txt files from the bank_effects_path to the working_directory_path
def copy_files(working_directory_path, bank_effects_path):
    # Check if the working directory exists
    if not os.path.exists(working_directory_path):
        # Create the working directory
        os.makedirs(working_directory_path)
    
    # Delete all files in the working directory
    for file in os.listdir(working_directory_path):
        os.remove(os.path.join(working_directory_path, file))
    
    # Copy .wav and .txt files from the bank_effects_path to the working directory
    for file in os.listdir(bank_effects_path):
        if file.endswith('.wav') or file.endswith('.txt'):
            shutil.copy(os.path.join(bank_effects_path, file), os.path.join(working_directory_path, file))
    # Check if there are any .wav or .txt files in the bank_effects_path
    if not any(file.endswith('.wav') or file.endswith('.txt') for file in os.listdir(bank_effects_path)):
        # Stop the script
        print("There are no .wav or .txt files in the bank_effects_path.")
        exit()


# Create a function to scan a directory for all audio formats (aac,m4a,mp3,ogg,wav, and any others) and create a list with each list entry containing the following: audioname with extension, full pathname to audio file, if the file was "replaced" with a0 for false and1 for true, and the length of the audio file in seconds
def scan_directory(directory, topdown=False):
    audio_list = []
    for root, dirs, files in os.walk(directory, topdown=topdown):
        for file in files:
            if file.endswith(('.aac', '.m4a', '.mp3', '.ogg', '.wav')):
                args=("ffprobe","-loglevel","8","-show_entries", "format=duration","-i",os.path.join(root, file))
                popen = subprocess.Popen(args, stdout = subprocess.PIPE)
                output = popen.stdout.read()
                audio_list.append([file, os.path.join(root, file), 0, float(output.decode().split('\n')[1].split('=')[1])])
    audio_list.sort(key=lambda x: x[3], reverse=True)
    return audio_list

def get_random_audio_by_length(audio_list, length, offset):
    # Create a sublist of the audio list with a length within the range of (length - offset) to (length + offset)
    sublist = [audio for audio in audio_list if audio[3] >= max(0.01, length - offset) and audio[3] <= length + offset]

    # If the sublist is empty, return None
    if not sublist:
        return None

    # Randomly pick a file from the sublist
    return random.choice(sublist)


def print_directory(directory):
  """Scans a directory and returns a list of all the files found."""
  files = []
  for root, dirs, filenames in os.walk(directory):
    for filename in filenames:
      print(filename)
      files.append(os.path.join(root, filename))
  return files


#create a function to take an audiolist and average the audio lengths and return the average
def average_audio_lengths(audio_list):
    total_length = 0
    for audio in audio_list:
        total_length += audio[3]
    return total_length / len(audio_list)

# Create a function to replace an audio file in a list with another audio file
def replace_audio(audio_list, old_audio, new_audio):
    for audio in audio_list:
        if audio[0] == old_audio:
            audio[1] = new_audio
            audio[2] = 1

meme_sound_effects_path = "/mnt/g/SteamLibrary/steamapps/common/Last Epoch/Last Epoch_Data/StreamingAssets/meme/meme_snd_eff/"
meme_music_path = '/mnt/g/SteamLibrary/steamapps/common/Last Epoch/Last Epoch_Data/StreamingAssets/meme/meme_music/'
bank_effects_path = "/mnt/g/SteamLibrary/steamapps/common/Last Epoch/Last Epoch_Data/StreamingAssets/Fmod Bank Tools.zip-2-0-0-1-4-1565765483/wav/Music"
working_directory_path = "/mnt/g/SteamLibrary/steamapps/common/Last Epoch/Last Epoch_Data/StreamingAssets/meme/bank_effects_working_directory/Music"

# Copy .wav and .txt files from the bank_effects_path to the working_directory_path
copy_files(working_directory_path, bank_effects_path)


meme_sound_effects_list = scan_directory(meme_sound_effects_path)
meme_music_list = scan_directory(meme_music_path)
bank_effects_list = scan_directory(bank_effects_path)

# # # Print the list variable name and then the first three rows and the last three rows of each audio file in the audio lists.  This will allow you to see the audio files in each list and the first and last three rows of each audio file in the list.
# print("meme_sound_effects_list:")
# print(meme_sound_effects_list[:3])
# print(meme_sound_effects_list[-3:])
# print("\nmeme_music_list:")
# print(meme_music_list[:3])
# print(meme_music_list[-3:])
# print("\nbank_effects_list:")
# print(bank_effects_list[:3])
# print(bank_effects_list[-3:])

#print the average time length for meme sounds, meme music, and bank effects in seconds
# print("Average meme sound length:", average_audio_lengths(meme_sound_effects_list))
# print("Average meme music length:", average_audio_lengths(meme_music_list))
# print("Average bank effect length:", average_audio_lengths(bank_effects_list))

