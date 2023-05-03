import os
from langchain.vectorstores import FAISS
import requests
from config import OPENAI_API_KEY, OPENAI_API_ENDPOINT, OPENAI_API_MODEL

# Set the headers for OpenAI
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}

def rewrite_text(prompt, prompt_style, supporting_data):
    if prompt_style:
        supporting_data = prompt_style + "\n" + supporting_data

    # Set the data for the primary OpenAI request
    data = {
        "model": OPENAI_API_MODEL,
        "messages": [
            {"role": "system", "content": supporting_data},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 2048,
        "presence_penalty": 0.6,
        "frequency_penalty": 0.6
    }

    if OPENAI_API_ENDPOINT == "https://api.openai.com/v1/completions":
        # Set the data for the OpenAI completions request
        data = {
            "model": OPENAI_API_MODEL,
            "prompt": f"{supporting_data}\n{prompt}",
            "temperature": 0.5,
            "max_tokens": 1000,
            "presence_penalty": 0.6,
            "frequency_penalty": 0.6
        }

    # Send the request to OpenAI
    response = requests.post(OPENAI_API_ENDPOINT, headers={"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}, json=data)

    # Handle the response
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        response.raise_for_status()

    response_json = response.json()

    if OPENAI_API_ENDPOINT == "https://api.openai.com/v1/completions":
        ai_response = response_json["choices"][0]["text"].strip()
    else:
        ai_response = response_json["choices"][0]["message"]["content"].strip()

    return ai_response
