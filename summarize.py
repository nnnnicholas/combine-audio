import os
import sys
import glob
import openai
from dotenv import load_dotenv
from pathlib import Path
from subprocess import call
import datetime

def main(directory):
    # Call transcribe.py
    try:
        call(["python3", "transcribe.py", directory])
    except Exception as e:
        print(f"Error executing transcribe.py: {e}")
        sys.exit(1)

    # Load OpenAI API Key
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("OPENAI_API_KEY not set in environment")
        sys.exit(1)
    openai.api_key = openai_api_key

    # Find the most recent transcript
    output_dir = os.path.join(directory, "output")
    transcript_files = glob.glob(os.path.join(output_dir, "Transcript_*.txt"))
    if not transcript_files:
        print("No transcript files found")
        sys.exit(1)
    latest_transcript = max(transcript_files, key=os.path.getctime)

    # Read the latest transcript content
    with open(latest_transcript, "r") as file:
        transcript_content = file.read()

    # Send the contents to OpenAI for summarization
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Please summarize the following transcript. Provide a 2 paragraph summary of the whole conversation and a bullet list of the top 10-15 topics discussed, in markdown format. The purpose of this summarization is to inform the writing of an introduction to a podcast, so feel free to include interesting rabbit holes in the list, even if they deviate from the overall theme of the show. Transcript: {transcript_content}"}
            ]
        )
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        sys.exit(1)

    if 'choices' in completion and len(completion.choices) > 0 and 'message' in completion.choices[0] and 'content' in completion.choices[0].message:
        summary = completion.choices[0].message["content"]
        print("Summary:")
        print(summary)

        # Write summary to file
        summary_filename = os.path.join(directory, f"Summary_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
        with open(summary_filename, "w") as file:
            file.write(summary)

        # Delete mp3 files
        mp3_files = glob.glob(os.path.join(output_dir, "*.mp3"))
        for mp3_file in mp3_files:
            os.remove(mp3_file)

    else:
        print("No summary available")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize.py <directory>")
        sys.exit(1)

    main(sys.argv[1])
