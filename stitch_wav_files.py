# Import required libraries
import os
import subprocess
import sys
import datetime

# Define the function to compress audio
def compress_audio(input_dir):
    # Define output directory
    output_dir = os.path.join(input_dir, "output")
    
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all files in the input directory
    for file_name in os.listdir(input_dir):
        # Check if file is a .wav file (case insensitive)
        if file_name.lower().endswith(".wav"):
            # Define the full path to the input file
            input_file = os.path.join(input_dir, file_name)

            # Get current timestamp and format it as a string
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # Define the full path to the output file, use the timestamp as file name
            output_file = os.path.join(output_dir, timestamp + '.mp3')

            # Use ffmpeg to convert the input file to a mp3 file with 64k bitrate, suitable for voice
            subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-ar", "44100", "-ac", "1", "-b:a", "64k", output_file])

# Main script
if __name__ == "__main__":
    # Check if the right number of command line arguments were provided
    if len(sys.argv) != 2:
        # If not, print usage information and exit
        print("Usage: python3 compress_audio.py <input_dir>")
        sys.exit(1)

    # Define the input directory as the first command line argument
    input_dir = sys.argv[1]

    # Call the function to compress audio
    compress_audio(input_dir)
