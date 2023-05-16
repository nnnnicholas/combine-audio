# Good for one-time sorting the outputs of the transcription process. Not necessary for most cases. 
import re
import sys

def extract_key(line):
    # Extract the key (file name) from the line
    match = re.search(r"Transcript for (.*?):", line)
    return match.group(1) if match else None

def sort_transcripts(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    transcripts = {}
    key = None

    # Iterate through the lines and create a dictionary of transcripts
    for line in lines:
        line = line.strip()
        new_key = extract_key(line)
        if new_key:
            key = new_key
            transcripts[key] = ""
        else:
            transcripts[key] += line

    # Sort the transcripts based on their keys (file names)
    sorted_transcripts = sorted(transcripts.items())

    # Write the sorted transcripts back into the file
    with open(file_path, 'w') as file:
        for key, value in sorted_transcripts:
            file.write(f"Transcript for {key}:\n{value}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]  # Get the file path from the command-line argument
        sort_transcripts(file_path)
    else:
        print("Usage: python script.py <path_to_file>")
