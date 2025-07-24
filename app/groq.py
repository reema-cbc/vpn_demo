import os
import requests
import tiktoken
from dotenv import load_dotenv, dotenv_values 
from fastapi import APIRouter, HTTPException
load_dotenv()
from typing import List
GROQ_API_KEY =os.getenv("my_key")
print(GROQ_API_KEY)
from typing import List

# Token-safe splitter
def split_transcript_by_tokens(text: str, max_tokens: int = 3000, model: str = "gpt-3.5-turbo") -> List[str]:
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

# Groq task generator for 1 chunk
def generate_tasks_from_transcript_with_groq(transcript: str) -> str:
    if not transcript.strip():
        return "Error: Transcript is empty."

    prompt = f"""
You are a helpful assistant. Based on the following video transcript, generate only a clear, concise list of actionable tasks in bullet points.
Do not include any narrative summary, headings, or explanation—just the task list in bullet form.

Transcript:
\"\"\"{transcript}\"\"\"
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert assistant that extracts only clean, bullet-point task lists from transcripts."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Network error: {str(e)}"
    except KeyError:
        return f"Unexpected response: {response.text}"

# Formatter function to clean bullet points
def format_bullet_tasks_dot_prefix(raw_bullets: str) -> List[str]:
    """
    Converts Groq-style • bullets into '.Sentence' style bullets.
    """
    lines = raw_bullets.split('\n')
    formatted = []

    for line in lines:
        line = line.lstrip("• ").strip()
        if not line:
            continue
        # Capitalize first letter and ensure it ends with a period
        line = line[0].upper() + line[1:]
        if not line.endswith('.'):
            line += '.'
        formatted.append(line)
        #formatted.append(f".{line}")

    return formatted

# Multi-chunk handler with formatting
def generate_tasks_from_large_transcript(transcript: str) -> str:
    chunks = split_transcript_by_tokens(transcript)
    all_tasks = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        tasks = generate_tasks_from_transcript_with_groq(chunk)
        all_tasks.append(tasks.strip())

    # Join and format
    joined_tasks = "\n".join(all_tasks)
    formatted = format_bullet_tasks_dot_prefix(joined_tasks)
    return "\n".join(formatted)








































































