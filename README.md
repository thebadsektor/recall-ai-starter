# Meeting Bot Tutorial

A Python application that uses [Recall.ai](https://recall.ai) to send a bot to Google Meet meetings, record transcripts, and download the conversation data.

## Features

- 🤖 Automatically join Google Meet meetings with a bot named "Pam"
- 📝 Real-time transcription using Recall.ai's streaming transcription
- 📥 Download and save meeting transcripts as JSON files
- 🔄 Poll bot status to track meeting progress

## Prerequisites

- Python 3.7+
- Recall.ai API key
- Google Meet meeting links

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd meeting-bot-tutorial
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install requests python-dotenv
```

4. Create a `.env` file in the project root:
```env
RECALL_API_KEY=your_recall_api_key_here
RECALL_REGION=us-west-2
```

## Usage

### Send Bot to Meeting

Run the main script to send Pam (the bot) to a Google Meet:

```bash
python main.py
```

You'll be prompted to enter a Google Meet link. The script will:
1. Create a bot and send it to the meeting
2. Wait for you to admit the bot to the meeting
3. Monitor the bot's status until the meeting ends
4. Display the bot ID for transcript retrieval

### Download Transcript

Once the meeting is complete, download the transcript using:

```bash
python get_transcript.py
```

Enter the bot ID when prompted. The transcript will be saved as `transcript_{bot_id}.json`.

## Project Structure

```
meeting-bot-tutorial/
├── main.py              # Main script to create and monitor meeting bot
├── get_transcript.py    # Script to fetch and save transcripts
├── .env                 # Environment variables (not tracked in git)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## API Reference

This project uses the [Recall.ai API](https://docs.recall.ai/) with the following endpoints:

- `POST /bot` - Create a new bot
- `GET /bot/{bot_id}` - Get bot status
- `GET /transcript/{transcript_id}` - Get transcript metadata

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RECALL_API_KEY` | Your Recall.ai API key | (required) |
| `RECALL_REGION` | Recall.ai API region | `us-west-2` |

## Notes

- The bot uses the name "Pam (Meeting Bot)" in meetings
- Transcripts use English (US) language code by default
- Meeting hosts need to manually admit the bot when it requests to join
- Bot status polling runs for approximately 2 minutes (24 attempts × 5 seconds)

## License

MIT
