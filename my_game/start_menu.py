import pygame
from config import SCREEN_W, SCREEN_H

# Menu settings
BENCH_SIZE = 5
TOTAL_COUNT_OPTIONS = [10, 15, 20, 25, 30]


# Draw start menu
def draw_start_menu(screen, font, selected_total, overlay=False):
    # Draw overlay
    if overlay:
        panel_w, panel_h = 560, 400
        panel_x = SCREEN_W // 2 - panel_w // 2
        panel_y = 70
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 175))
        pygame.draw.rect(panel, (255, 255, 255, 60), panel.get_rect(), 2, border_radius=20)
        screen.blit(panel, (panel_x, panel_y))
    else:
        screen.fill((20, 20, 20))

    # Draw title
    big_font = pygame.font.SysFont("Arial", 48)
    title = big_font.render("Pokemon Card Game", True, (255, 204, 0))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 90))

    # Draw label
    label_font = pygame.font.SysFont("Arial", 22)
    label = label_font.render("Choose total cards per player:", True, (255, 255, 255))
    screen.blit(label, (SCREEN_W // 2 - label.get_width() // 2, 190))

    # Draw hint
    hint_font = pygame.font.SysFont("Arial", 15)
    deck_size = selected_total - BENCH_SIZE
    hint = hint_font.render(
        f"{BENCH_SIZE} on the field + {deck_size} in the deck = {selected_total} total",
        True, (170, 170, 170)
    )
    screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 220))

    # Button layout
    buttons = []
    btn_w, btn_h = 64, 64
    gap = 16
    total_w = len(TOTAL_COUNT_OPTIONS) * btn_w + (len(TOTAL_COUNT_OPTIONS) - 1) * gap
    start_x = SCREEN_W // 2 - total_w // 2
    y = 270

    # Draw card options
    count_font = pygame.font.SysFont("Arial", 24)
    for i, total in enumerate(TOTAL_COUNT_OPTIONS):
        x = start_x + i * (btn_w + gap)
        is_selected = total == selected_total

        # Button colors
        bg = (255, 204, 0) if is_selected else (60, 60, 60)
        border = (255, 255, 255) if is_selected else (120, 120, 120)
        text_color = (20, 20, 20) if is_selected else (255, 255, 255)

        # Draw option
        pygame.draw.rect(screen, bg, (x, y, btn_w, btn_h), border_radius=12)
        pygame.draw.rect(screen, border, (x, y, btn_w, btn_h), 2, border_radius=12)

        # Draw number
        text = count_font.render(str(total), True, text_color)
        screen.blit(text, (x + btn_w // 2 - text.get_width() // 2, y + btn_h // 2 - text.get_height() // 2))

        # Save button
        buttons.append((x, y, btn_w, btn_h, total))

    # Start button
    start_btn_w, start_btn_h = 220, 60
    start_x_btn = SCREEN_W // 2 - start_btn_w // 2
    start_y_btn = y + btn_h + 60

    # Draw start button
    pygame.draw.rect(screen, (46, 139, 87), (start_x_btn, start_y_btn, start_btn_w, start_btn_h), border_radius=14)
    pygame.draw.rect(screen, (255, 255, 255), (start_x_btn, start_y_btn, start_btn_w, start_btn_h), 2, border_radius=14)

    # Draw start text
    start_font = pygame.font.SysFont("Arial", 30)
    start_text = start_font.render("START", True, (255, 255, 255))
    screen.blit(
        start_text,
        (start_x_btn + start_btn_w // 2 - start_text.get_width() // 2,
         start_y_btn + start_btn_h // 2 - start_text.get_height() // 2)
    )

    # Save start button
    start_button = (start_x_btn, start_y_btn, start_btn_w, start_btn_h)

    # Update screen
    pygame.display.flip()
    return buttons, start_button


# Check card option
def get_clicked_total(pos, buttons):
    for x, y, w, h, total in buttons:
        if x < pos[0] < x + w and y < pos[1] < y + h:
            return total
    return None


# Check start click
def is_start_clicked(pos, start_button):
    if start_button is None:
        return False

    x, y, w, h = start_button
    return x < pos[0] < x + w and y < pos[1] < y + h