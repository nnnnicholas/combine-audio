import os
import argparse
import logging
from tqdm import tqdm
import subprocess

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def stitch_files(directory, output_bitrate="128k"):
    # Get a list of all .wav files (case-insensitive) in the directory
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.wav')])

    # Check if the directory is empty or contains no .wav files
    if not files:
        raise ValueError("The specified directory is empty or contains no .wav files")

    # Write the file paths to a list file for ffmpeg
    list_file = "wav_files.txt"
    with open(list_file, "w") as f:
        for file in tqdm(files, desc='Preparing files'):  # Adding progress bar
            f.write(f"file '{os.path.join(directory, file)}'\n")

    # Combine and convert all .wav files into one .mp3 file
    output_file = "output.mp3"
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', output_bitrate, output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Clean up the list file
    os.remove(list_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine WAV files into an MP3.')
    parser.add_argument('-d', '--directory', type=str, required=True,
                        help='Directory containing WAV files to be combined')

    args = parser.parse_args()

    try:
        stitch_files(args.directory)
    except ValueError as e:
        logging.error(str(e))  # log to the file
        print(str(e))  # also print the error message
    except IndexError as e:
        logging.error("Unexpected error: " + str(e))  # log to the file
        print("Unexpected error:", str(e))  # also print the error message
