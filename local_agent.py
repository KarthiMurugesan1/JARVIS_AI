import os
import subprocess
import pyautogui
import shutil
import platform
import send2trash
import time

def open_file(filepath):
    if os.path.exists(filepath):
        if platform.system() == "Darwin":  # macOS
            subprocess.call(["open", filepath])
        elif platform.system() == "Windows":
            os.startfile(filepath)
        else:
            subprocess.call(["xdg-open", filepath])
        return f"📂 Opened: {filepath}"
    else:
        return "❌ File not found."

def search_files(keyword, directory=os.path.expanduser("~")):
    matches = []
    for root, _, files in os.walk(directory):
        for f in files:
            if keyword.lower() in f.lower():
                matches.append(os.path.join(root, f))
    return matches or ["❌ No files found."]

def delete_file(filepath):
    if os.path.exists(filepath):
        send2trash.send2trash(filepath)
        return f"🗑️ Moved to Trash: {filepath}"
    return "❌ File not found."

def open_app(app_name):
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.call(["open", f"/Applications/{app_name}.app"])
        elif platform.system() == "Windows":
            subprocess.Popen([app_name])
        else:
            subprocess.call([app_name])
        return f"🚀 Opened: {app_name}"
    except Exception as e:
        return f"❌ Could not open {app_name}: {e}"

def type_text(text):
    pyautogui.write(text, interval=0.05)
    return f"📝 Typed: {text}"
