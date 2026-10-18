import json
import os
from config import CHATS_FOLDER

os.makedirs(CHATS_FOLDER, exist_ok=True)

def save_chat(chat_id, messages):
    file_path = os.path.join(CHATS_FOLDER, f"{chat_id}.json")
    with open(file_path, "w", encoding="utf-8") as write:
        json.dump(messages, write, ensure_ascii=False, indent=4)

def load_chat(chat_id):
    file_path = os.path.join(CHATS_FOLDER, f"{chat_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as read:
            return json.load(read)
    return []