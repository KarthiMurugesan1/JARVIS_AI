# memory_updater.py

import os
import json
import requests
import re
from dotenv import load_dotenv
from memory_manager import update_memory, get_memory
from config import OPENROUTER_API_KEY, LLM_MODEL

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = os.getenv("LLM_MODEL")

def extract_fact_from_input(user_input):
    """
    Ask LLM to detect memory update intent and return action.
    Example expected:
    {"action": "update", "key": "goal", "value": "become an AI expert"}
    """
    system_prompt = """
You are a memory controller agent. From the user's sentence:
- If they want to **update memory**, return JSON like:
  {"action": "update", "key": "goal", "value": "become an AI expert"}
- If no update intent found, return {}
Only return a JSON. No explanation or markdown.
"""

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_input.strip()}
    ]

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": messages,
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 512
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print("🔍 LLM raw output:", content)

        match = re.search(r'\{.*?\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("❌ Memory update error:", e)

    return {}

def extract_and_update(user_input):
    fact = extract_fact_from_input(user_input)
    if not fact or "action" not in fact:
        return "⚠️ No valid memory update found."

    action = fact["action"]
    key = fact.get("key")
    value = fact.get("value")

    if action == "update" and key and value:
        return update_memory(key, value)

    return "⚠️ Invalid update format or missing data."
