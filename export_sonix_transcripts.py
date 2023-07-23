import os
import requests
import json
from tqdm import tqdm
from sonix_credentials import API_KEY, BASE_URL


def fetch_transcript(media_id):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    url = f"{BASE_URL}/v1/media/{media_id}/transcript"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch transcript for Media ID: {media_id}")
        return None


def save_transcript(media_id, transcript):
    file_path = os.path.join("transcripts", f"{media_id}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(transcript)


def main():
    os.makedirs("transcripts", exist_ok=True)

    # Dummy media IDs, replace this with your actual media IDs from sonix.ai account
    media_ids = ["media_id_1", "media_id_2", "media_id_3"]

    print("Fetching and saving transcripts...")
    for media_id in tqdm(media_ids):
        transcript_data = fetch_transcript(media_id)
        if transcript_data:
            transcript_text = transcript_data.get("text", "")
            save_transcript(media_id, transcript_text)

    print("Transcripts have been exported successfully!")


if __name__ == "__main__":
    main()
