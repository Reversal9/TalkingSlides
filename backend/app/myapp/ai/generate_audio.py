from pathlib import Path
from openai import OpenAI
import os
from . import generate_text
from io import BytesIO
from pydub import AudioSegment

voice_options = ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]

def add_voice(input_script, voice_opt1):
    '''
    voice_options = ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]
    if not (voice in voice_options):
        voice_opt = "alloy"
    else:
        voice_opt = voice 
    '''
    voice_opt = voice_opt1
    
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
    requests = 0
    speaker_one_scripts, speaker_two_scripts = generate_text.extract_speaker_texts(script_text)
    speaker_one_responses = []
    speaker_two_responses = []
    total_responses = []

    filenum = 0
    for text in speaker_one_scripts:
      if (requests > 20):
        return total_responses
      response = client.audio.speech.create(
          model="tts-1",
          voice=voice_opt1,
          input=text,
      )
      requests += 1
      # response.stream_to_file(f"speaker1{filenum}.mp3")
      filenum += 1
      if not (response and response.content):
        return None
      speaker_one_responses.append(response.content)

    filenum = 0
    for text in speaker_two_scripts: 
      if (requests > 20): 
        return total_responses
      response = client.audio.speech.create(
          model="tts-1",
          voice=voice_opt2,
          input=text,
      )
      requests += 1
      # response.stream_to_file(f"speaker2{filenum}.mp3")
      filenum += 1
      if not (response and response.content):
        return None
      speaker_two_responses.append(response.content)

    i = 0
    while speaker_one_responses or speaker_two_responses:
      if speaker_one_responses and speaker_two_responses:
          if i % 2 == 0:
            total_responses.append(speaker_one_responses.pop(0))
          else:
            total_responses.append(speaker_two_responses.pop(0))
      if speaker_one_responses:
            total_responses.append(speaker_one_responses.pop(0))
      else:
            total_responses.append(speaker_two_responses.pop(0))

      i += 1

    combined = AudioSegment.empty()

    for file in total_responses:
        audio_data = BytesIO(file)
        audio_segment = AudioSegment.from_mp3(audio_data)
        combined += audio_segment  # Concatenate

    output_buffer = BytesIO()
    combined.export(output_buffer, format="mp3")
    output_buffer.seek(0)

    return output_buffer
