import pygame
import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

def _load_volume():
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return float(data.get("volume", 0.1))
    except (FileNotFoundError, ValueError, KeyError):
        return 0.1

def _save_volume(volume):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"volume": volume}, f)
    except Exception:
        pass

def init_sound():
    pygame.mixer.init()

def play_music(path, loop=True):
    volume = _load_volume()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if loop else 0)

def set_volume(volume):
    pygame.mixer.music.set_volume(volume)
    _save_volume(volume)

def toggle_mute():
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music._last_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0)
        _save_volume(0)
    else:
        restored = getattr(pygame.mixer.music, '_last_volume', 0.5)
        pygame.mixer.music.set_volume(restored)
        _save_volume(restored)