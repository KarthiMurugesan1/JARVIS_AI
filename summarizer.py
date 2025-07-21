from memory_manager import get_memory
from togenther_api import query_deepseek
from datetime import datetime

def summarize_today_conversation(history):
    today = datetime.now().date()
    today_msgs = [m for m in history if m.get("timestamp") and datetime.fromisoformat(m["timestamp"]).date() == today]
    if not today_msgs:
        return "No conversation so far today."

    convo = "\n".join([f'{m["role"].upper()}: {m["content"]}' for m in today_msgs])
    prompt = f"Summarize this conversation between user and Jarvis:\n\n{convo}"
    return query_deepseek([{"role": "user", "content": prompt}])

def summarize_web_result(query: str, web_result: str) -> str:
    if not web_result or len(web_result.strip()) < 20:
        return "Sorry, the web result was too short to summarize."

    memory = get_memory()
    relevant_info = "\n".join([
        f"{k}: {v}" for k, v in memory.items()
        if any(word in query.lower() for word in [k.lower(), "dad", "mom", "city", "location"])
    ])

    prompt = f"""
You are Jarvis, an intelligent assistant.

User context:
{relevant_info}

Summarize the following web results in 2–3 sentences based on the user's query.

User Query: {query}

Web Result:
{web_result}

Be clear, concise, and optionally personalize if relevant.
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant named Jarvis."},
        {"role": "user", "content": prompt}
    ]

    try:
        return query_deepseek(messages).strip() + "\n\n📎 Source: Brave Search"
    except Exception as e:
        print("⚠️ Summarization failed:", e)
        return "Sorry, I couldn't summarize that result."
