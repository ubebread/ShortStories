# story_writer/app/story_engine.py
import os
import requests

OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama3')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/generate')

def generate_story(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', '')
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except (requests.exceptions.RequestException, KeyError, ValueError):
        return None