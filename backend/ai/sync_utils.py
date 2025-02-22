import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SYNC_API_KEY")
url = "https://api.sync.so/v2/generate"

def run_sync(video_url, audio_url, webhook_url):
    payload = {
        "model": "lipsync-1.7.1",
        "input": [
            {
                "type": "video",
                "url": "url"
            },
            {
                "type": "audio",
                "url": "url"
            }
        ],
        "options": {
            "pads": [0, 5, 0, 0],
            "speedup": 1,
            "output_format": "mp4",
            "sync_mode": "bounce",
            "fps": 25,
            "output_resolution": [1280, 720],
            "active_speaker": True
        },
        "webhookUrl": "https://your-server.com/webhook"
    }
    headers = {
        "x-api-key": "<api-key>",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)