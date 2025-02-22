import openai

from openai import OpenAI

system_prompt = """
You are a 
"""

script_formatter = """
You are a helpful assistant. You will be provided with a document delimited by triple quotes.
Your goal is to convert the text in the document to a presentation script for a video.
Divide the script into sections that are at most 3 minutes long. Include markers to indicate
a new section in the script in the format [Section #N].
"""
def parse_pdf(filename):
    

def create_script(input_text):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": system_prompt},
            {
                "role": "user",
                "content": "Convert this text into a script."
            }
        ],
        prediction={
            "type": "content",
            "content": script_formatter
        }
    )

    print(completion.choices[0].message)