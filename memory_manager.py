import json, os

MEMORY_FILE = "memory.json"

def log_memory_change(key, old_value, new_value):
    with open("memory_log.json", "a") as f:
        log_entry = {"key": key, "old": old_value, "new": new_value}
        f.write(json.dumps(log_entry) + "\n")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(key, value):
    memory = load_memory()
    old_value = memory.get(key.lower())
    memory[key.lower()] = value
    save_memory(memory)

    if old_value:
        log_memory_change(key, old_value, value)

    return f"✅ Memory updated: {key} → {value}"


def get_memory():
    return load_memory()
