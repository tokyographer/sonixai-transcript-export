import os
import requests
import json
import time
from tqdm import tqdm
from sonix_credentials import SONIX_API_KEY, SONIX_API_URL

def export_transcripts():
    # Create a folder named "transcripts" if it doesn't exist
    if not os.path.exists("transcripts"):
        os.makedirs("transcripts")

    # Get the list of all transcripts
    headers = {"Authorization": f"Bearer {SONIX_API_KEY}"}
    response = requests.get(f"{SONIX_API_URL}/v1/files", headers=headers)
    transcripts_data = json.loads(response.text)

    # Extract transcript IDs and filenames
    transcript_ids = [item["id"] for item in transcripts_data["data"]]

    # Export transcripts one by one and save them as text files
    for transcript_id in tqdm(transcript_ids, desc="Exporting Transcripts"):
        response = requests.get(f"{SONIX_API_URL}/v1/files/{transcript_id}/content", headers=headers)

        # Check if the API request was successful
         if response.status_code == 200:
            transcript_data = json.loads(response.text)
            filename = f"transcripts/{transcript_data['data']['name']}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                    file.write(transcript_data["data"]["content"])
        else:
            print(f"Error exporting transcript {transcript_id}. Status Code: {response.status_code}")
            print("Response content:", response.text)


if __name__ == "__main__":
    start_time = time.time()

    export_transcripts()

    end_time = time.time()
    duration = end_time - start_time
    print(f"Transcripts exported successfully! Total duration: {duration:.2f} seconds.")
