import os
import sys

def get_nexus_root():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_dir

def get_usb_root():
    return os.path.dirname(get_nexus_root())

def ensure_directories(username=None):
    nexus_root = get_nexus_root()
    if username:
        user_root = os.path.join(nexus_root, 'data', 'users', username)
        dirs = [
            user_root,
            os.path.join(user_root, 'notes'),
        ]
    else:
        dirs = [
            os.path.join(nexus_root, 'data'),
            os.path.join(nexus_root, 'data', 'notes'),
            os.path.join(nexus_root, 'config'),
            os.path.join(nexus_root, 'logs'),
            os.path.join(nexus_root, 'assets'),
        ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def get_data_path(filename, username=None):
    if username:
        return os.path.join(get_nexus_root(), 'data', 'users', username, filename)
    return os.path.join(get_nexus_root(), 'data', filename)

def get_notes_path(username=None):
    if username:
        return os.path.join(get_nexus_root(), 'data', 'users', username, 'notes')
    return os.path.join(get_nexus_root(), 'data', 'notes')

def get_config_path(filename):
    return os.path.join(get_nexus_root(), 'config', filename)

def get_models_dir():
    return os.path.join(get_nexus_root(), 'models')
