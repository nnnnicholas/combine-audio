import os
import argparse
import logging
from pydub import AudioSegment
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def convert_wav_to_mp3(file, directory, intermediate_bitrate="64k"):
    wav_path = os.path.join(directory, file)
    wav_audio = AudioSegment.from_wav(wav_path)
    intermediate_file = os.path.splitext(file)[0] + "_intermediate.mp3"
    wav_audio.export(intermediate_file, format="mp3", bitrate=intermediate_bitrate)
    return intermediate_file

def stitch_files(directory, intermediate_bitrate="64k"):
    # Get a list of all .wav files (case-insensitive) in the directory
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.wav')])

    # Check if the directory is empty or contains no .wav files
    if not files:
        raise ValueError("The specified directory is empty or contains no .wav files")

    # Convert each .wav file to an intermediate .mp3 file with 64 kbps bitrate
    intermediate_files = process_map(lambda file: convert_wav_to_mp3(file, directory, intermediate_bitrate),
                                     files, desc="Converting .wav files to .mp3", unit="file")
    # Load the first intermediate .mp3 file
    combined = AudioSegment.from_mp3(intermediate_files[0])

    # Append all subsequent intermediate .mp3 files
    for file in tqdm(intermediate_files[1:], desc="Combining .mp3 files", unit="file"):
        combined += AudioSegment.from_mp3(file)

    # Export the combined audio to a single 64 kbps .mp3 file
    combined.export("output.mp3", format="mp3", bitrate="64k")

    # Clean up the intermediate .mp3 files
    for file in intermediate_files:
        os.remove(file)


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