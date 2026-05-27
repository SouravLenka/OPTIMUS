import os
import json
import threading

class AssistantConfig:
    def __init__(self):
        self.lock = threading.Lock()
        # Resolve config path relative to main workspace root
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        self.config_path = os.path.join(self.root_dir, 'config.json')
        self.settings = {}
        self.load_defaults()
        self.load_config()

    def load_defaults(self):
        self.settings = {
            "assistant_name": "OPTIMUS",
            "voice_rate": 175,
            "voice_volume": 1.0,
            "voice_profile": "male-deep",
            "sound_effects": True,
            "mic_device_index": None,
            "mic_sensitivity": 70,
            "theme": "default-cyber",
            "scanlines": True,
            "bg_particles": True,
            "continuous_listening": True,
            "eel_rpc": True,
            "start_minimised": False,
            "openai_api_key": "",
            "groq_api_key": ""
        }

    def load_config(self):
        with self.lock:
            if not os.path.exists(self.config_path):
                self.save_config_unsafe()
                return

            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                    # Merge to ensure all keys exist
                    self.settings.update(user_settings)
            except Exception as e:
                print(f"[ERROR] Failed loading config.json, resetting to defaults: {e}")
                self.save_config_unsafe()

    def get(self, key, default=None):
        with self.lock:
            return self.settings.get(key, default)

    def set(self, key, value):
        with self.lock:
            self.settings[key] = value
            self.save_config_unsafe()

    def update_settings(self, new_settings_dict):
        with self.lock:
            self.settings.update(new_settings_dict)
            self.save_config_unsafe()

    def save_config_unsafe(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Failed writing to config.json: {e}")

# Global configuration instance
config = AssistantConfig()

def load_config():
    """Return the global AssistantConfig instance for easy import."""
    return config
