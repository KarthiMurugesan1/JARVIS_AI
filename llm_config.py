# llm_config.py
import os

llm_config = {
    "config_list": [
        {
            "model": os.getenv("LLM_MODEL"),
            "base_url": "https://api.together.xyz/v1",
            "api_key": os.getenv("TOGETHER_API_KEY"),
        }
    ],
    "temperature": 0.7,
    "cache_seed": 42,
}
