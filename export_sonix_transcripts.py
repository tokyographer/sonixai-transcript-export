import os
import requests
from tqdm import tqdm
import time

# Function to fetch transcript and save to a file
def fetch_and_save_transcript(id):
    url = f"https://api.sonix.ai/v1/media/{id}/transcript.txt"
    response = requests.get(url)

    if response.status_code == 200:
        with open(f"transcript_{id}.txt", "w", encoding="utf-8") as file:
            file.write(response.text)

# Read the list of ids from the sonixmedia.txt file
def read_ids_from_file(file_path):
    with open(file_path, "r") as file:
        ids = [line.strip() for line in file]
    return ids

def main():
    file_path = "sonixmedia.txt"
    ids = read_ids_from_file(file_path)

    total_ids = len(ids)
    print(f"Total number of ids: {total_ids}\n")

    start_time = time.time()

    # Using tqdm to create a progress bar
    with tqdm(total=total_ids, desc="Fetching Transcripts", unit="id") as pbar:
        for id in ids:
            fetch_and_save_transcript(id)
            pbar.update(1)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nTranscripts fetched and saved in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
