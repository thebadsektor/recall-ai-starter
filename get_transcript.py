import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RECALL_API_KEY")
BASE_URL = "https://us-west-2.recall.ai/api/v1"

def fetch_transcript_from_bot(bot_id: str):
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY,
    }

    # Step 1: Get bot info
    print(f"Fetching bot info for Bot ID: {bot_id}...")
    bot_url = f"{BASE_URL}/bot/{bot_id}/"
    bot_response = requests.get(bot_url, headers=headers)
    bot_response.raise_for_status()
    bot_data = bot_response.json()

    # Step 2: Get transcript ID from recordings
    recordings = bot_data.get("recordings", [])
    if not recordings:
        raise ValueError("❌ No recordings found for this bot.")

    transcript_id = None
    for rec in recordings:
        transcript_info = rec.get("media_shortcuts", {}).get("transcript")
        if transcript_info and "id" in transcript_info:
            transcript_id = transcript_info["id"]
            break

    if not transcript_id:
        raise ValueError("❌ No transcript found in bot recordings.")

    print(f"✅ Found Transcript ID: {transcript_id}")

    # Step 3: Fetch transcript metadata
    transcript_url = f"{BASE_URL}/transcript/{transcript_id}/"
    transcript_response = requests.get(transcript_url, headers=headers)
    transcript_response.raise_for_status()
    transcript_meta = transcript_response.json()

    download_url = transcript_meta.get("data", {}).get("download_url")
    if not download_url:
        raise ValueError("❌ No download URL found — transcript may not be ready yet.")

    # Step 4: Fetch actual transcript JSON from the download URL
    print("Downloading actual transcript data...")
    transcript_data_response = requests.get(download_url)
    transcript_data_response.raise_for_status()
    transcript_data = transcript_data_response.json()

    # Step 5: Save transcript JSON locally
    filename = f"transcript_{bot_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Full transcript saved to {filename}")


if __name__ == "__main__":
    bot_id = input("Enter Bot ID: ").strip()
    fetch_transcript_from_bot(bot_id)