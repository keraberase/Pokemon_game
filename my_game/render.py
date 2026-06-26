import pygame
from config import *
from game_logic import *
from trash import *
from endscreen import *
from attack_menu import draw_attack_menu


def render(game):
    game.screen.blit(game.background, (0, 0))

    ex, ey = ZONES["enemy_battle"]
    if game.enemy_on_field:
        draw_text(game.screen, game.font, f"HP: {game.enemy_hp()}", (ex, ey - 25))
        game.screen.blit(game.enemy_images[game.enemy_index], (ex, ey))

    px, py = ZONES["player_battle"]
    battle_i = get_battle_index(game.card_locations)
    if battle_i is not None:
        game.screen.blit(game.player_images[battle_i], (px, py))
        draw_text(game.screen, game.font, f"HP: {game.player_hps[battle_i]}", (px, py - 25))

    bx, by = ZONES["player_bench_start"]
    for i, image in enumerate(game.player_images):
        if game.card_locations[i] != "bench":
            continue
        if i == game.dragged_card_index and game.dragging:
            continue
        offset_y = -15 if game.hovered_card_index == i else 0
        game.screen.blit(image, (bx + i * BENCH_STEP, by + offset_y))

    ebx, eby = ZONES["enemy_bench_start"]
    bench_count = sum(1 for loc in game.enemy_locations if loc == "bench")
    for i in range(bench_count):
        game.screen.blit(game.card_back, (ebx + i * BENCH_STEP, eby))

    draw_trash(game.screen, game.card_back, game.card_locations, game.enemy_locations, ZONES)

    if game.dragging and game.dragged_card_index is not None:
        game.screen.blit(game.player_images[game.dragged_card_index], (game.drag_pos[0] - 45, game.drag_pos[1] - 51))

    # pokeball volume button (rendered BEFORE preview overlay so card hides it)
    if not game.game_over:
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        volume = pygame.mixer.music.get_volume()
        color = (154, 15, 36) if volume > 0 else (100, 100, 100)

        pygame.draw.circle(game.screen, (50, 50, 50), (cx, cy + 4), 40)
        pygame.draw.circle(game.screen, color, (cx, cy), 40)
        pygame.draw.circle(game.screen, (141, 8, 25), (cx, cy), 40, 3)

        if game.show_volume_bar:
            bar_h = 150
            bar_w = 10
            bar_x = cx + 50
            bar_y = cy - bar_h

            pygame.draw.rect(game.screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
            fill_h = int(bar_h * volume)
            pygame.draw.rect(game.screen, (141, 8, 25), (bar_x, bar_y + bar_h - fill_h, bar_w, fill_h), border_radius=5)

            vol_text = game.font.render(f"{int(volume * 100)}%", True, (255, 255, 255))
            game.screen.blit(vol_text, (bar_x - 10, bar_y - 25))

    if game.preview_card is not None and game.preview_image is not None:
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        game.screen.blit(overlay, (0, 0))
        game.screen.blit(game.preview_image, (275, 125))

    # mouse_pos = pygame.mouse.get_pos()
    # game.screen.blit(game.font.render(f"X:{mouse_pos[0]} Y:{mouse_pos[1]}", True, (255, 255, 0)), (10, 10))
    # game over
    if game.game_over:
        if game.game_result == "win":
            draw_end_screen(game.screen, game.font, "YOU WIN!", (255, 215, 0))
        else:
            draw_end_screen(game.screen, game.font, "YOU LOSE!", (255, 0, 0))


    if game.attack_menu_open:
        attacks = game.player_deck[game.pending_attack_card_index].get("attacks", [])
        game.attack_menu_buttons = draw_attack_menu(game.screen, game.font, attacks)
    

    draw_log(game.screen, game.font, game.battle_log, game.show_battle_log, game.log_scroll)


    pygame.display.flip()