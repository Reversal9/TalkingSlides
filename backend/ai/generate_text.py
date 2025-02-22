import pymupdf
import openai
from openai import OpenAI

system_prompt = """
You are a helpful assistant. You will be provided with a document delimited by triple quotes.
Your goal is to convert the text in the document to a presentation script for a video.
Divide the script into sections that are at most 3 minutes long. Include markers to indicate
a new section in the script in the format [Section #N].
"""

script_formatter = """

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
        
def create_script(input_text):
    client = OpenAI()

    script = ""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": system_prompt},
            {
                "role": "user",
                "content": "Convert this text into a script."
            }
        ],
        stream=True,
        prediction={
            "type": "content",
            "content": script_formatter
        }
    )

    for chunk in completions:
        script += completion.choices[0].message
        
    return script