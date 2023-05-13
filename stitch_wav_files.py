import os
import subprocess
import sys
import datetime

def compress_audio(input_dir):
    output_dir = os.path.join(input_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".wav"):
            input_file = os.path.join(input_dir, file_name)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_file = os.path.join(output_dir, timestamp + '.mp3')

            # Use ffmpeg to convert to mp3 with 64k bitrate, suitable for voice
            subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-ar", "44100", "-ac", "1", "-b:a", "64k", output_file])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 compress_audio.py <input_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]

    compress_audio(input_dir)
