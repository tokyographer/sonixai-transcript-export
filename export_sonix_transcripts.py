import os
import requests
from tqdm import tqdm
import time
import concurrent.futures
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
        "Authorization": f"Bearer {SONIX_API_KEY}",
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response.status_code == 200:
            if "transcript" in response_json:
                return id, response_json["transcript"]
            else:
                print(f"Error for ID {id}: No transcript found in the response.")
        else:
            print(f"Error for ID {id}: Status Code {response.status_code}")
            print(response_json)  # Print the full response to check for details
    except requests.exceptions.RequestException as e:
        print(f"Error for ID {id}: {e}")
    except ValueError as ve:
        print(f"Error for ID {id}: Invalid JSON response")
        print(f"Response Content: {response.text}")

# Progress bar setup
total_ids = len(ids)
progress_bar = tqdm(total=total_ids, unit="id", desc="Transcribing")

# Timer start
start_time = time.time()

# Concurrently fetch transcripts using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Use a dictionary to keep track of transcript results
    transcript_results = {id: transcript for id, transcript in executor.map(get_transcript, ids)}

# Iterate through the results and save transcripts to files
for id, transcript in transcript_results.items():
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
