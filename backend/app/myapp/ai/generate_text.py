import pymupdf
import openai
from openai import OpenAI
import os
import re


system_prompt_duo = """
You are a helpful assistant. You will be provided with a document delimited by triple quotes.
Your goal is to convert the text in the document to a presentation script for a video.
Divide the script into sections that are at most 3 minutes long. Assign each second to two different speakers,
speaker 1 and speaker 2. Label each section with [SPEAKER #1] or [SPEAKER #2]. The two speakers are having a discussion
with each other and building off of each others' ideas. 
"""

system_prompt_solo = """
You are a helpful assistant. You will be provided with a document delimited by triple quotes.
Your goal is to convert the text in the document to a presentation script for a video.
Divide the script into sections that are at most 3 minutes long. The script should be like a single-person podcast.
""" 

script_formatter_duo = """
[SPEAKER #1]
Line of dialogue. 

[SPEAKER #2]
Line of dialogue.
"""
script_formatter_solo = """

"""
def parse_pdf(filename):
    delimited_text = ""
    doc = pymupdf.open(filename)
    num_pages = doc.page_count
    page_num = 0
    for page in doc: 
        page_text = page.get_text("blocks")  
        for block in page_text:
            delimited_text += block
            delimited_text += "[Section {page_num}]\n"
        page_num += 1
    return delimited_text

def parse_pdf_binary(binary_content):
    doc = pymupdf.open(stream=binary_content,filetype="pdf")
    delimited_text = ""
    num_pages = doc.page_count
    page_num = 0
    for page in doc: 
        page_text = page.get_text("blocks")  
        for block in page_text:
            delimited_text += block[4]
            delimited_text += "[Section {page_num}]\n"
        page_num += 1
    doc.close()
    return delimited_text

def extract_speaker_texts(text):
    speaker_one_texts = []
    speaker_two_texts = []
    
    # Define regex pattern to capture alternating dialogue
    pattern = re.findall(r"\[SPEAKER #1\](.*?)(?=\[SPEAKER #2\]|$)|\[SPEAKER #2\](.*?)(?=\[SPEAKER #1\]|$)", text, re.DOTALL)
    
    for match in pattern:
        speaker_one_text, speaker_two_text = match
        if speaker_one_text:
            speaker_one_texts.append(speaker_one_text.strip())
        if speaker_two_text:
            speaker_two_texts.append(speaker_two_text.strip())
    
    return speaker_one_texts, speaker_two_texts
        
def generate_script(input_text, input_prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    script = ""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": system_prompt_solo},
            {
                "role": "user",
                "content": f"Convert these lecture notes into a presentation script, {input_prompt}.Here are the notes: {input_text}"
            }
        ],
        stream=True,
        prediction={
            "type": "content",
            "content": script_formatter
        }
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            script += chunk.choices[0].delta.content
        
    return script


def generate_script_duo(input_text, input_prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    script = ""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": system_prompt_duo},
            {
                "role": "user",
                "content": f"Convert these lecture notes into a presentation script with these specifications: {input_prompt}. Here are the notes: {input_text}.",
            }
        ],
        stream=True,
        prediction={
            "type": "content",
            "content": script_formatter_duo
        }
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            script += chunk.choices[0].delta.content
        
    return script