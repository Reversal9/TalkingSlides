import requests
import os
import modal
import diffusers
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
from dotenv import load_dotenv

load_dotenv()
sync_api_key = os.getenv("SYNC_API_KEY")
sync_url = "https://api.sync.so/v2/generate"

app = modal.App(name="video-generator")

# try to use GPU acceleration
@app.function(gpu="A100")
def create_video_from_text(export_path, webhook_url):
    input_prompt = """
    A helpful instructor giving a lecture.
    """
    pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", 
                                             torch_dtype=torch.float16, 
                                             variant="fp16")
    pipe = pipe.to("cuda")
    pipe.enable_model_cpu_offload()

    # memory optimization
    # https://github.com/huggingface/diffusers/issues/6869#issuecomment-1929569492
    
    pipe.unet.enable_forward_chunking(chunk_size=1, dim=1)
    pipe.enable_vae_slicing()
    video_frames = pipe(input_prompt, num_frames=24).frames[0]
    try:
        video_path = export_to_video(video_frames, fps=10, output_video_path=export_path)
        payload = {"status" : "success", "video_path" : video_path}
    except Exception as e: 
        payload = {"status" : "error", "video_path" : str(e)} 

    response = requests.post(webhook_url, json=payload)
'''
# image to video function in case text doesn't work
@app.function()
def create_video_from_img(img_url):
'''

@app.function(gpu="A100")
def run_sync(video_url, audio_url, webhook_url):
    payload = {
        "model": "lipsync-1.7.1",
        "input": [
            {
                "type": "video",
                "url": video_url
            },
            {
                "type": "audio",
                "url": audio_url
            }
        ],
        "options": {
            "pads": [0, 5, 0, 0],
            "speedup": 2,
            "output_format": "mp4",
            "sync_mode": "cutoff",
            "fps": 25,
            "output_resolution": [1080, 720],
            "active_speaker": True
        },
        "webhookUrl": webhook_url
    }
    headers = {
        "x-api-key": sync_api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", sync_url, json=payload, headers=headers)

    print(response.text)
    
    