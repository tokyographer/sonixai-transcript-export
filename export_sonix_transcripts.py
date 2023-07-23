import os
import requests
from tqdm import tqdm
from sonix_credentials import SONIX_API_KEY

# Base URL for Sonix API
SONIX_API_BASE_URL = "https://api.sonix.ai/v1"

# Function to get all transcripts from Sonix.ai
def get_transcripts(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Fetch all transcripts using Sonix.ai API
    response = requests.get(f"{SONIX_API_BASE_URL}/transcripts", headers=headers)
    response.raise_for_status()

    return response.json()["results"]

# Function to export transcript text to a file
def export_transcript_to_file(transcript):
    filename = os.path.join("transcripts", f"{transcript['name']}.txt")

    # Write the transcript content to a text file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(transcript["content"])

# Main function
def main():
    try:
        # Create the 'transcripts' directory if it doesn't exist
        os.makedirs("transcripts", exist_ok=True)

        # Get the list of transcripts
        transcripts = get_transcripts(SONIX_API_KEY)

        # Display progress bar and export transcripts
        print("Exporting transcripts:")
        for transcript in tqdm(transcripts, unit="transcript"):
            export_transcript_to_file(transcript)

        print("Transcripts exported successfully!")
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
