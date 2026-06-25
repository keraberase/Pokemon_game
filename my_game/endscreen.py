import pygame
from config import SCREEN_W, SCREEN_H

def draw_end_screen(screen, font, message, color):
    
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    
    big_font = pygame.font.SysFont("Arial", 72)
    text = big_font.render(message, True, color)
    x = (SCREEN_W - text.get_width()) // 2
    y = (SCREEN_H - text.get_height()) // 2
    screen.blit(text, (x, y))

    
    small_text = font.render("ESC - exit  |  R - restart", True, (200, 200, 200))
    screen.blit(small_text, ((SCREEN_W - small_text.get_width()) // 2, y + 100))

    pygame.display.flip()