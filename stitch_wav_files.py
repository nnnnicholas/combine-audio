import os
import argparse
from pydub import AudioSegment
from tqdm import tqdm

def stitch_files(directory):
    # Get a list of all .wav files (case-insensitive) in the directory
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.wav')])

    # Check if the directory is empty or contains no .wav files
    if not files:
        raise ValueError("The specified directory is empty or contains no .wav files")

    # Load the first file
    combined = AudioSegment.from_wav(os.path.join(directory, files[0]))

    # Append all subsequent files with a progress bar
    for f in tqdm(files[1:], desc="Combining audio files", unit="file"):
        combined += AudioSegment.from_wav(os.path.join(directory, f))

    # Export to mp3
    combined.export("output.mp3", format="mp3", bitrate="128k")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine WAV files into an MP3.')
    parser.add_argument('-d', '--directory', type=str, required=True,
                        help='Directory containing WAV files to be combined')

    args = parser.parse_args()

    try:
        stitch_files(args.directory)
    except ValueError as e:
        print(str(e))
    except IndexError as e:
        print("Unexpected error:", str(e))