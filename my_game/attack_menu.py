# attack_menu.py
import pygame
from config import SCREEN_W, SCREEN_H
from game_logic import get_damage, draw_text

def draw_attack_menu(screen, font, attacks):
    
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    
    big_font = pygame.font.SysFont("Arial", 36)
    title = big_font.render("Choose Attack", True, (255, 215, 0))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 150))

    
    buttons = []
    for i, atk in enumerate(attacks):
        name = atk.get("name", "Unknown")
        dmg = get_damage(atk)
        text = f"{name}  —  {dmg} dmg"

        btn_w, btn_h = 400, 50
        btn_x = SCREEN_W // 2 - btn_w // 2
        btn_y = 220 + i * 70

        
        pygame.draw.rect(screen, (60, 60, 60), (btn_x, btn_y, btn_w, btn_h), border_radius=10)
        pygame.draw.rect(screen, (255, 215, 0), (btn_x, btn_y, btn_w, btn_h), 2, border_radius=10)

        # Текст
        btn_text = font.render(text, True, (255, 255, 255))
        screen.blit(btn_text, (btn_x + 20, btn_y + 15))

        buttons.append((btn_x, btn_y, btn_w, btn_h, i))

    draw_text(screen, font, "ESC - cancel", (SCREEN_W // 2 - 50, 500), (150, 150, 150))
    return buttons


def get_clicked_attack(pos, buttons):
    for btn_x, btn_y, btn_w, btn_h, index in buttons:
        if btn_x < pos[0] < btn_x + btn_w and btn_y < pos[1] < btn_y + btn_h:
            return index
    return None