import pygame
from config import SCREEN_W, SCREEN_H

def draw_loading(screen, font, message="Loading...", progress=0, total=1):
    screen.fill((20, 20, 20))

    
    
    pokeball = pygame.image.load("images/pokeball.png")
    pokeball = pygame.transform.scale(pokeball, (200, 200))
    px = (SCREEN_W - 200) // 2
    py = (SCREEN_H - 200) // 2 - 50
    screen.blit(pokeball, (px, py))
    
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