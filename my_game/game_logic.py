from config import *
import pygame


# Get attack damage
def get_damage(atk):
    digits = ''.join(filter(str.isdigit, atk.get("damage", "")))
    return int(digits) if digits else 10


# Find battle card
def get_battle_index(card_locations):
    return next((i for i in range(len(card_locations)) if card_locations[i] == "battle"), None)


# Check mouse hit
def hit_test(pos, x, y, w=CARD_W, h=CARD_H):
    return x < pos[0] < x + w and y < pos[1] < y + h


# Draw text
def draw_text(screen, font, text, pos, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), pos)


# Log limit
MAX_LOGS = 5


# Add log
def add_log(game, message):
    game.battle_log.append(message)


# Small font
_small_font = None


# Draw log
def draw_log(screen, font, battle_log, show, scroll=0):
    global _small_font

    # Create font
    if _small_font is None:
        _small_font = pygame.font.SysFont("Arial", 14)

    # Log layout
    log_w = 180
    log_h = MAX_LOGS * 22 + 10
    log_x = LOG_X
    log_y = LOG_Y

    # Draw toggle
    arrow = "▼ Log" if show else "▶ Log"
    arrow_text = _small_font.render(arrow, True, (255, 255, 0))
    screen.blit(arrow_text, (log_x, log_y))

    # Skip empty log
    if not show or not battle_log:
        return

    # Draw background
    overlay = pygame.Surface((log_w, log_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (log_x, log_y))

    # Draw messages
    visible = battle_log[scroll:scroll + MAX_LOGS]
    for i, msg in enumerate(visible):
        text = _small_font.render(msg, True, (255, 255, 255))
        screen.blit(text, (log_x + 5, log_y + 5 + i * 22))