# main.py

import time
import requests
from tqdm import tqdm
from sonix_credentials import SONIX_API_KEY

def get_transcript_ids():
    api_url = "https://api.sonix.ai/v1/transcripts"

    headers = {
        "Authorization": f"Bearer {SONIX_API_KEY}",
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch transcripts.")
        print(response.text)
        return []

def get_transcript_text(transcript_id):
    api_url = f"https://api.sonix.ai/v1/transcripts/{transcript_id}/plain"

    headers = {
        "Authorization": f"Bearer {SONIX_API_KEY}",
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch transcript with ID {transcript_id}.")
        print(response.text)
        return None

if __name__ == "__main__":
    start_time = time.time()
    transcripts = get_transcript_ids()

    if transcripts:
        num_transcripts = len(transcripts)
        print(f"Fetching {num_transcripts} transcripts...")
        for transcript in tqdm(transcripts):
            transcript_id = transcript['id']
            transcript_text = get_transcript_text(transcript_id)

            if transcript_text:
                print(f"Transcript ID: {transcript_id}")
                print(f"Transcript Text: {transcript_text}")
                print("----")

    end_time = time.time()
    duration = end_time - start_time
    print(f"Process completed in {duration:.2f} seconds.")
