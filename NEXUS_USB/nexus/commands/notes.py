import os
import json
import uuid
from datetime import datetime
from nexus.core.utils import get_notes_path

def _get_notes_file(username=None):
    return os.path.join(get_notes_path(username), 'notes.json')

def _load_notes(username=None):
    notes_file = _get_notes_file(username)
    if os.path.exists(notes_file):
        try:
            with open(notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_notes(notes, username=None):
    notes_file = _get_notes_file(username)
    try:
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2)
    except Exception as e:
        return str(e)
    return None

def notes_list(username=None):
    notes = _load_notes(username)
    if not notes:
        return "No notes found."
    lines = ["NOTES:"]
    for note in notes:
        lines.append(f"- [{note.get('id','')}] {note.get('title','Untitled')} ({note.get('created','')})")
    return "\n".join(lines)

def notes_add(title, content, username=None):
    notes = _load_notes(username)
    note = {
        'id': str(uuid.uuid4())[:8],
        'title': title or 'Untitled',
        'content': content or '',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    notes.append(note)
    err = _save_notes(notes, username)
    if err:
        return f"Error saving note: {err}"
    return f"Note created: {note['id']}"

def notes_search(query, username=None):
    notes = _load_notes(username)
    query = query.lower()
    matches = [n for n in notes if query in n.get('title','').lower() or query in n.get('content','').lower()]
    if not matches:
        return "No matching notes found."
    lines = ["MATCHES:"]
    for note in matches:
        lines.append(f"- [{note.get('id','')}] {note.get('title','Untitled')}")
    return "\n".join(lines)

def notes_delete(note_id, username=None):
    notes = _load_notes(username)
    new_notes = [n for n in notes if n.get('id') != note_id]
    if len(new_notes) == len(notes):
        return "Note not found."
    err = _save_notes(new_notes, username)
    if err:
        return f"Error deleting note: {err}"
    return f"Note deleted: {note_id}"
