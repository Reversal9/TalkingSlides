from pathlib import Path
from openai import OpenAI
import os
import generate_text

def add_voice(input_script):
    '''
    voice_options = ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]
    if not (voice in voice_options):
        voice_opt = "alloy"
    else:
        voice_opt = voice 
    '''
    voice_opt = "alloy"
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_opt,
        input=input_script,
    ) 

    if response and response.content:
        return response.content

    return None

def add_voice_dialogue(script_text, voice_opt1, voice_opt2):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    speaker_one_scripts, speaker_two_scripts = generate_text.extract_speaker_texts(script_text)
    speaker_one_responses = []
    speaker_two_responses = []

    filenum = 0
    for text in speaker_one_scripts: 
      response = client.audio.speech.create(
          model="tts-1",
          voice=voice_opt1,
          input=text,
      ) 
      # response.stream_to_file(f"speaker_1_{filenum}.mp3")
      filenum += 1
      if not (response and response.content):
        return None
      speaker_one_responses.append(response.content)

    filenum = 0
    for text in speaker_two_scripts: 
      response = client.audio.speech.create(
          model="tts-1",
          voice=voice_opt2,
          input=text,
      ) 
      # response.stream_to_file(f"speaker_2_{filenum}.mp3")
      filenum += 1
      if not (response and response.content):
        return None
      speaker_two_responses.append(response.content)

    return speaker_one_responses, speaker_two_responses

