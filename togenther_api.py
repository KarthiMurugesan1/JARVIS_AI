# together_api.py

import os
import requests
from dotenv import load_dotenv
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3.1-70B")  # Or your preferred model

def query_deepseek(messages=None, system_role="You are a helpful personal assistant named Jarvis."):
    url = "https://api.together.xyz/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🛡️ Fix: If passed a string instead of message list
    if isinstance(messages, str):
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": messages}
        ]

    if messages is None:
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": "Hello!"}
        ]

    payload = {
        "model": TOGETHER_MODEL,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Together API error: {http_err}")
        print("👉 Response:", response.text)
    except Exception as e:
        print("❌ General API error:", e)

    return "Sorry, I couldn't process that right now."

