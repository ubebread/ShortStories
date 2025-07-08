# story_writer/app/story_engine.py
import requests

def generate_story(prompt):
    # Only use local Ollama model
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json()['response']