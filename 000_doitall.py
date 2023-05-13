import os
import subprocess
import sys
import openai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the function to compress the audio
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
                print(f"Error occurred while compressing {input_file}: {str(e)}")
                continue

    return output_dir

# Function to call Whisper API for each file in the output directory
def call_whisper_api(output_dir):
    transcript_file_path = os.path.join(output_dir, 'transcript.txt')
    with open(transcript_file_path, 'w') as transcript_file:
        for filename in os.listdir(output_dir):
            if filename.lower().endswith('.mp3'):
                audio_file_path = os.path.join(output_dir, filename)
                with open(audio_file_path, 'rb') as audio_file:
                    try:
                        transcript = openai.Audio.translate("whisper-1", audio_file)
                        transcript_file.write(f'Transcript for {filename}:\n')
                        transcript_file.write(f'{transcript}\n\n')
                    except Exception as e:
                        print(f"Error occurred while translating {audio_file_path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input directory>")
        sys.exit(1)

    output_dir = compress_audio(sys.argv[1])
    call_whisper_api(output_dir)
