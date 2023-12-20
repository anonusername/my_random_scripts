# Create a python script that acts as a wrapper for the command "yt-dlp". Here is the github page for yt-dlp you can use for reference. https://github.com/yt-dlp/yt-dlp What I mean about a wrapper is that the python script will accept all input given by the user and pass it to a new yt-dlp command instance


import subprocess
import sys
import os

def main():
    # Get the input from the user.
    input_args = sys.argv[1:]

    # Check if the yt-dlp command is already installed.
    if not subprocess.call(["which", "yt-dlp"]):
        raise Exception("The yt-dlp command is not installed. Please install it and try again.")

    # Remove any "-F" and "--list-formats" flags from the input arguments.
    if "--best" in input_args:
        input_args.remove("-F")
        #input_args.remove("--list-formats")
        input_args.append("-F")

    # Pass the input to the yt-dlp command.
    subprocess.call(["yt-dlp"] + input_args)

if __name__ == "__main__":
    # # Figure out where the file is already via the os.
    # file_path = os.path.dirname(os.path.realpath(__file__))

    # # Add the file path to the sys.path.
    # sys.path.append(file_path)

    main()
