import pygame
import json
import os

# Settings path
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

# Saved volume
_last_volume = 0.5


# Load volume
def _load_volume():
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return float(data.get("volume", 0.1))
    except (FileNotFoundError, ValueError, KeyError):
        return 0.1


# Save volume
def _save_volume(volume):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"volume": volume}, f)
    except Exception:
        pass


# Init sound
def init_sound():
    pygame.mixer.init()


# Play music
def play_music(path, loop=True):
    volume = _load_volume()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if loop else 0)


# Set volume
def set_volume(volume):
    pygame.mixer.music.set_volume(volume)
    _save_volume(volume)


# Toggle mute
def toggle_mute():
    global _last_volume

    if pygame.mixer.music.get_volume() > 0:
        # Mute music
        _last_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0)
        _save_volume(0)
    else:
        # Restore volume
        pygame.mixer.music.set_volume(_last_volume)
        _save_volume(_last_volume)