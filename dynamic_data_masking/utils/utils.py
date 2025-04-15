import os

def find_file(directory, ext):
    ext = ext if ext.startswith('.') else f".{ext}"
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and entry.lower().endswith(ext.lower()):
            return full_path
    return None