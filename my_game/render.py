import pygame
from config import *
from game_logic import *
from trash import *
from endscreen import *
from attack_menu import draw_attack_menu


# Draw game
def render(game):
    # Draw background
    game.screen.blit(game.background, (0, 0))

    # Draw enemy card
    ex, ey = ZONES["enemy_battle"]
    if game.enemy_on_field and game.enemy_index < len(game.enemy_images):
        draw_text(game.screen, game.font, f"HP: {game.enemy_hp()}", (ex, ey - 25))
        game.screen.blit(game.enemy_images[game.enemy_index], (ex, ey))

    # Draw player card
    px, py = ZONES["player_battle"]
    battle_i = get_battle_index(game.card_locations)
    if battle_i is not None:
        game.screen.blit(game.player_images[battle_i], (px, py))
        draw_text(game.screen, game.font, f"HP: {game.player_hps[battle_i]}", (px, py - 25))

    # Draw player bench
    bx, by = ZONES["player_bench_start"]
    for i, image in enumerate(game.player_images):
        if game.card_locations[i] != "bench":
            continue
        if i == game.dragged_card_index and game.dragging:
            continue

        # Hover lift
        offset_y = -15 if game.hovered_card_index == i else 0
        game.screen.blit(image, (bx + i * game.bench_step, by + offset_y))

    # Draw player deck
    if game.player_deck_pile:
        game.screen.blit(game.card_back, ZONES["player_deck"])

    # Count enemy bench
    ebx, eby = ZONES["enemy_bench_start"]
    visible_enemy_bench = 0

    for i in range(game.enemy_index + 1, len(game.enemy_locations)):
        if game.enemy_locations[i] == "bench":
            visible_enemy_bench += 1

    # Draw enemy bench
    for index in range(visible_enemy_bench):
        game.screen.blit(game.card_back, (ebx + index * game.bench_step, eby))

    # Draw enemy deck
    if game.enemy_deck_pile:
        game.screen.blit(game.card_back, ZONES["enemy_deck"])

    # Draw trash
    draw_trash(
        game.screen,
        game.card_back,
        game.card_locations,
        game.enemy_locations,
        ZONES,
        game.player_trash_count,
        game.enemy_trash_count
    )

    # Draw volume button
    if not game.game_over:
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        volume = pygame.mixer.music.get_volume()
        color = (154, 15, 36) if volume > 0 else (100, 100, 100)

        # Draw button
        pygame.draw.circle(game.screen, (50, 50, 50), (cx, cy + 4), 40)
        pygame.draw.circle(game.screen, color, (cx, cy), 40)
        pygame.draw.circle(game.screen, (141, 8, 25), (cx, cy), 40, 3)

        # Draw volume bar
        if game.show_volume_bar:
            bar_h = 150
            bar_w = 10
            bar_x = cx + 50
            bar_y = cy - bar_h

            pygame.draw.rect(game.screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)

            # Fill volume
            fill_h = int(bar_h * volume)
            pygame.draw.rect(
                game.screen,
                (141, 8, 25),
                (bar_x, bar_y + bar_h - fill_h, bar_w, fill_h),
                border_radius=5
            )

            # Draw percent
            vol_text = game.font.render(f"{int(volume * 100)}%", True, (255, 255, 255))
            game.screen.blit(vol_text, (bar_x - 10, bar_y - 25))

    # Draw preview
    if game.preview_card is not None and game.preview_image is not None:
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        game.screen.blit(overlay, (0, 0))
        game.screen.blit(game.preview_image, (275, 125))

    # Debug mouse
    # mouse_pos = pygame.mouse.get_pos()
    # game.screen.blit(game.font.render(f"X:{mouse_pos[0]} Y:{mouse_pos[1]}", True, (255, 255, 0)), (10, 10))

    # Draw end screen
    if game.game_over:
        if game.game_result == "win":
            draw_end_screen(game.screen, game.font, "YOU WIN!", (255, 215, 0))
        else:
            draw_end_screen(game.screen, game.font, "YOU LOSE!", (255, 0, 0))

    # Draw attack menu
    if game.attack_menu_open:
        attacks = game.player_bench[game.pending_attack_card_index].get("attacks", [])
        game.attack_menu_buttons = draw_attack_menu(game.screen, game.font, attacks)

    # Draw battle log
    draw_log(game.screen, game.font, game.battle_log, game.show_battle_log, game.log_scroll)

    # Draw dragged card
    if game.dragging and game.dragged_card_index is not None:
        game.screen.blit(
            game.player_images[game.dragged_card_index],
            (game.drag_pos[0] - 45, game.drag_pos[1] - 51)
        )

    # Update screen
    pygame.display.flip()