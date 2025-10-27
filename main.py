import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RECALL_API_KEY = os.getenv("RECALL_API_KEY")
RECALL_REGION = os.getenv("RECALL_REGION", "us-west-2")
BASE_URL = f"https://{RECALL_REGION}.recall.ai/api/v1"

def create_bot(meeting_url):
    print("Booking Pam (Meeting Bot) for the meeting....")
    url = f"{BASE_URL}/bot"
    headers = {"Authorization": f"Token {RECALL_API_KEY}"}
    payload = {
        "meeting_url": meeting_url,
        "bot_name": "Pam (Meeting Bot)",
        "recording_config": {
            "transcript": {
                "provider": {
                    "recallai_streaming": {
                        "language_code": "en_us"
                    }
                }
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Pam cannot join the meeting. Please check the following (this is worse than a typo): {response.text}")
    return response.json()

def get_bot_status(bot_id):
    url = f"{BASE_URL}/bot/{bot_id}"
    headers = {"Authorization": f"Token {RECALL_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Pam's line is unreachable. Failed to get bot status")
    return response.json()

def get_transcript_url(bot_id):
    url = f"{BASE_URL}/bot/{bot_id}/recording"
    headers = {"Authorization": f"Token {RECALL_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Pam's binder cannot be accessed! Failed to get transcript")
    return response.json().get("transcript", {}).get("url")

def main():
    # Ask user for meeting URL
    meeting_url = input("Enter Google Meet link: ").strip()
    if not meeting_url:
        print("❌ Meeting link is required.")
        return

    print(f"\nMeeting URL: {meeting_url}")
    print(f"API Region: {RECALL_REGION}\n")

    try:
        bot = create_bot(meeting_url)
        bot_id = bot["id"]
        print(f"✅ Bot created successfully!")
        print(f"Bot ID: {bot_id}\n")
        print("Waiting for Pam to join the meeting...\n")

        # Poll for meeting completion
        for attempt in range(24):  # ~2 minutes
            status_data = get_bot_status(bot_id)
            status_changes = status_data.get("status_changes", [])
            if status_changes:
                code = status_changes[-1].get("code", "")
            else:
                code = ""

            print(f"[{(attempt + 1) * 5}s] Bot status: {code}")

            if code == "done":
                print("\n✅ Pam has completed the call.\n")
                break
            elif code == "fatal":
                print("❌ Pam is not at her desk! Bot encountered a fatal error.")
                return
            elif code == "joining_call":
                print("ℹ️ Knock! Knock! - Please let Pam in the meeting.")
            
            time.sleep(5)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check your API key, meeting URL, or .env setup.")

if __name__ == "__main__":
    main()