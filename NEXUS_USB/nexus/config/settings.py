import json
import os
from nexus.core.utils import get_config_path, get_data_path

DEFAULT_CONFIG = {
    "username": "achyut",
    "password": "200712",
    "ai_engine": "rule",
    "local_model_enabled": False,
    "local_model_path": "",
    "theme": "dark",
    "exhibition_mode": False,
    "font_family": "Consolas",
    "font_size": 11,
    "users": {
        "achyut": {"password": "200712"},
        "guest": {"password": "guest"}
    },
}

class Settings:
    def __init__(self):
        self.config_file = get_config_path('settings.json')
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                self.data.update(loaded)
            except Exception:
                pass

    def save(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get_users(self):
        return self.data.get('users', {})

    def add_user(self, username, password):
        users = self.get_users()
        users[username] = {"password": password}
        self.set('users', users)

    def verify_user(self, username, password):
        users = self.get_users()
        user = users.get(username)
        if user and user.get('password') == password:
            return True
        return False

    def user_exists(self, username):
        return username in self.get_users()

settings = Settings()
