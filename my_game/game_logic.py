from config import *
import pygame


def get_damage(atk):
    digits = ''.join(filter(str.isdigit, atk.get("damage", "")))
    return int(digits) if digits else 10

def do_attack(defender_hp, damage):
    return max(0, defender_hp - damage)

def get_battle_index(card_locations):
    return next((i for i in range(5) if card_locations[i] == "battle"), None)

def hit_test(pos, x, y, w=CARD_W, h=CARD_H):
    return x < pos[0] < x + w and y < pos[1] < y + h

def draw_text(screen, font, text, pos, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), pos)


MAX_LOGS = 5 

def add_log(game, message):
    game.battle_log.append(message)
    



def draw_log(screen, font, battle_log, show, scroll=0):

    small_font = pygame.font.SysFont("Arial", 14)
    log_w = 180
    log_h = MAX_LOGS * 22 + 10
    log_x = LOG_X
    log_y = LOG_Y

    arrow = "▼ Log" if show else "▶ Log"
    arrow_text = small_font.render(arrow, True, (255, 255, 0))
    screen.blit(arrow_text, (log_x, log_y))

    if not show or not battle_log:
        return
    
    overlay = pygame.Surface((log_w, log_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (log_x, log_y))

    
    
    visible = battle_log[scroll:scroll + MAX_LOGS]
    for i, msg in enumerate(visible):
        text = small_font.render(msg, True, (255, 255, 255))
        screen.blit(text, (log_x + 5, log_y + 5 + i * 22))