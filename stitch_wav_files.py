import os
import argparse
from pydub import AudioSegment

def stitch_files(directory):
    # Get a list of all .wav files in the directory
    files = sorted([f for f in os.listdir(directory) if f.endswith('.wav')])

    # Load the first file
    combined = AudioSegment.from_wav(os.path.join(directory, files[0]))

    # Append all subsequent files
    for f in files[1:]:
        combined += AudioSegment.from_wav(os.path.join(directory, f))

    # Export to mp3
    combined.export("output.mp3", format="mp3", bitrate="128k")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine WAV files into an MP3.')
    parser.add_argument('-d', '--directory', type=str, required=True,
                        help='Directory containing WAV files to be combined')

    args = parser.parse_args()
    stitch_files(args.directory)