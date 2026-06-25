import pygame

def init_sound():
    pygame.mixer.init()

def play_music(path, volume=0.1, loop=True):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if loop else 0)  

def set_volume(volume):
    pygame.mixer.music.set_volume(volume)  

def toggle_mute():
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music._last_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(getattr(pygame.mixer.music, '_last_volume', 0.5))