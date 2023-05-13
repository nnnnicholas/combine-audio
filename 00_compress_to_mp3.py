## COMPRESS TO MONO 64kbps MP3

import os
import subprocess
import logging

# Setting up logging
logging.basicConfig(filename='compress_audio.log', level=logging.ERROR, format='%(asctime)s %(levelname)s - %(message)s')

def compress_audio(input_dir):
    output_dir = os.path.join(input_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.wav'):
            input_file = os.path.join(input_dir, filename)
            compressed_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.mp3")

            # Compress the file
            try:
                subprocess.run(['ffmpeg', '-i', input_file, '-map_channel', '0.0.0', '-ac', '1', '-ar', '44100', '-b:a', '64k', compressed_file], check=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error occurred while compressing {input_file}: {e}")
                continue

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input directory>")
        sys.exit(1)

    compress_audio(sys.argv[1])
