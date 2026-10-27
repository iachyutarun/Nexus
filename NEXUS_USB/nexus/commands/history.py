import os
from nexus.core.utils import get_data_path

def _get_history_file(username=None):
    return get_data_path('history.json', username)

def _load_history(username=None):
    history_file = _get_history_file(username)
    if os.path.exists(history_file):
        try:
            import json
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_history(history, username=None):
    history_file = _get_history_file(username)
    try:
        import json
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def add_history(command, username=None):
    history = _load_history(username)
    history.append({'command': command, 'time': ''})
    _save_history(history, username)

def get_history(username=None):
    history = _load_history(username)
    if not history:
        return "No command history."
    return "\n".join(f"{i+1}. {h['command']}" for i, h in enumerate(history))

def clear_history(username=None):
    _save_history([], username)
    return "History cleared."
