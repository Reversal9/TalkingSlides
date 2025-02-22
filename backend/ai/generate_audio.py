from pathlib import Path
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def add_voice(input_script, speech_file_path, voice):
    voice_options = ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]
    if not (voice in voice_options):
        voice_opt = "alloy"
    else:
        voice_opt = voice 
      
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_opt,
        input=input_script,
    )
    response.stream_to_file(speech_file_path)
    

