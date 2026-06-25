import pygame
from config import *
from game_logic import *
from trash import *

def render(game):
    game.screen.blit(game.background, (0, 0))

    ex, ey = ZONES["enemy_battle"]
    draw_text(game.screen, game.font, f"HP: {game.enemy_hp}", (ex, ey - 25))
    game.screen.blit(game.enemy_image, (ex, ey))

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
    for i in range(4):
        game.screen.blit(game.card_back, (ebx + i * BENCH_STEP, eby))

    draw_trash(game.screen, game.player_images, game.card_back, game.card_locations, game.enemy_locations, ZONES)

    if game.dragging and game.dragged_card_index is not None:
        game.screen.blit(game.player_images[game.dragged_card_index], (game.drag_pos[0] - 45, game.drag_pos[1] - 51))

    if game.preview_card is not None and game.preview_image is not None:
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        game.screen.blit(overlay, (0, 0))
        game.screen.blit(game.preview_image, (275, 125))
        draw_text(game.screen, game.font, "ESC - close", (310, 490), (200, 200, 200))

    mouse_pos = pygame.mouse.get_pos()
    game.screen.blit(game.font.render(f"X:{mouse_pos[0]} Y:{mouse_pos[1]}", True, (255, 255, 0)), (10, 10))

    pygame.display.flip()