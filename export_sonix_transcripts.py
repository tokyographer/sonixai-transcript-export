import os
import requests
from tqdm import tqdm
import time

from sonix_credentials import SONIX_API_KEY

SONIX_API_BASE_URL = "https://api.sonix.ai"
OUTPUT_DIRECTORY = "transcripts"
INPUT_FILE = "sonixids.txt"

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Read the list of ids from the input file
with open(INPUT_FILE, "r") as f:
    ids = f.read().splitlines()

def get_transcript(id):
    url = f"{SONIX_API_BASE_URL}/v1/media/{id}/transcript"
    headers = {
        "Authorization": "SONIX_API_KEY",  # Replace with your Sonix API key
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response.status_code == 200:
            return response_json["transcript"]
        else:
            print(f"Error for ID {id}: Status Code {response.status_code}")
            print(response_json)  # Print the full response to check for details
    except requests.exceptions.RequestException as e:
        print(f"Error for ID {id}: {e}")

# Progress bar setup
total_ids = len(ids)
progress_bar = tqdm(total=total_ids, unit="id", desc="Transcribing")

# Timer start
start_time = time.time()

# Iterate through each ID and get the transcript
for id in ids:
    transcript = get_transcript(id)
    if transcript:
        with open(f"{OUTPUT_DIRECTORY}/{id}_transcript.txt", "w") as f:
            f.write(transcript)
    progress_bar.update(1)

# Timer end
end_time = time.time()
execution_time = end_time - start_time

# Close the progress bar
progress_bar.close()

print(f"\nTranscription completed for {total_ids} IDs.")
print(f"Total execution time: {execution_time:.2f} seconds.")
