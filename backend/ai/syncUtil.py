import requests

url = "https://api.sync.so/v2/generate"

payload = {
    "model": "lipsync-1.7.1",
    "input": [
        {
            "type": "video",
            "url": "https://synchlabs-public.s3.us-west-2.amazonaws.com/david_demo_shortvid-03a10044-7741-4cfc-816a-5bccd392d1ee.mp4"
        },
        {
            "type": "audio",
            "url": "https://synchlabs-public.s3.us-west-2.amazonaws.com/david_demo_shortaud-27623a4f-edab-4c6a-8383-871b18961a4a.wav"
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