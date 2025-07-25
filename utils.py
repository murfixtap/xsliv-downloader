import os
import re


def sanitize_folder_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def sanitize_filename(name: str) -> str:
    name = name.strip().lower().replace(" ", "_")
    return re.sub(r'[^a-z0-9_]', '', name)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
