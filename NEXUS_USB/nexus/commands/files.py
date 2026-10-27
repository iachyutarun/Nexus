import os
from nexus.core.utils import get_nexus_root, get_data_path

ALLOWED_BASE = get_nexus_root()

def list_files(path=None):
    base = os.path.join(ALLOWED_BASE, 'data') if path is None else os.path.join(ALLOWED_BASE, path)
    if not os.path.exists(base):
        return "Path not found."
    if os.path.isfile(base):
        return base
    entries = sorted(os.listdir(base))
    if not entries:
        return "Directory is empty."
    lines = [f"  {e}" for e in entries]
    return "\n".join(lines)

def search_files(query):
    base = os.path.join(ALLOWED_BASE, 'data')
    if not os.path.exists(base):
        return "Data directory not found."
    matches = []
    for root, dirs, files in os.walk(base):
        for name in files + dirs:
            if query.lower() in name.lower():
                rel = os.path.relpath(os.path.join(root, name), ALLOWED_BASE)
                matches.append(rel)
    if not matches:
        return "No matches found."
    return "\n".join(matches)
