import pygame
from config import SCREEN_W, SCREEN_H

_pokeball_image = None

def draw_loading(screen, font, message="Loading...", progress=0, total=1):
    global _pokeball_image
    screen.fill((20, 20, 20))

    if _pokeball_image is None:
        try:
            raw_img = pygame.image.load("images/pokeball.png")
            _pokeball_image = pygame.transform.scale(raw_img, (200, 200))
        except pygame.error:
            # fallback
            _pokeball_image = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(_pokeball_image, (220, 50, 50), (100, 100), 100)
            pygame.draw.rect(_pokeball_image, (240, 240, 240), (0, 100, 200, 100))
            pygame.draw.line(_pokeball_image, (50, 50, 50), (0, 100), (200, 100), 10)
            pygame.draw.circle(_pokeball_image, (50, 50, 50), (100, 100), 30)
            pygame.draw.circle(_pokeball_image, (255, 255, 255), (100, 100), 15)

    px = (SCREEN_W - 200) // 2
    py = (SCREEN_H - 200) // 2 - 50
    screen.blit(_pokeball_image, (px, py))
    
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, ((SCREEN_W - text.get_width()) // 2, py + 220))
    
    bar_w = 400
    bar_h = 20
    bar_x = (SCREEN_W - bar_w) // 2
    bar_y = py + 260

    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=10)

    fill_w = int(bar_w * (progress / total))
    if fill_w > 0:
        pygame.draw.rect(screen, (255, 200, 0), (bar_x, bar_y, fill_w, bar_h), border_radius=10)

    pygame.display.flip()