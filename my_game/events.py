from config import *
from game_logic import *
from card_utils import *
from trash import *

def process_mouse_down(game, pos, now):
    bx, by = ZONES["player_bench_start"]
    px, py = ZONES["player_battle"]
    ex, ey = ZONES["enemy_battle"]

    for i in range(5):
        if game.card_locations[i] != "bench":
            continue
        card_x = bx + i * BENCH_STEP
        if hit_test(pos, card_x, by):
            if game.last_click_index == i and now - game.last_click_time < 400:
                game.preview_card = i
                game.preview_image = load_large_image(game.player_deck[i])
            else:
                game.dragging = True
                game.dragged_card_index = i
                game.drag_from = "bench"
                game.drag_pos = pos
                game.last_click_time = now
                game.last_click_index = i
            return

    battle_i = get_battle_index(game.card_locations)
    if battle_i is not None and hit_test(pos, px, py):
        if game.last_click_index == battle_i and now - game.last_click_time < 400:
            game.preview_card = battle_i
            game.preview_image = load_large_image(game.player_deck[battle_i])
        else:
            game.dragging = True
            game.dragged_card_index = battle_i
            game.drag_from = "battle"
            game.drag_pos = pos
            game.last_click_time = now
            game.last_click_index = battle_i
        return

    if hit_test(pos, ex, ey):
        if game.last_click_index == "enemy" and now - game.last_click_time < 400:
            game.preview_card = "enemy"
            game.preview_image = load_large_image(game.enemy_card)
        game.last_click_time = now
        game.last_click_index = "enemy"

def process_mouse_motion(game, pos):
    if game.dragging:
        game.drag_pos = pos
    else:
        game.hovered_card_index = None
        bx, by = ZONES["player_bench_start"]
        for i in range(5):
            if game.card_locations[i] != "bench":
                continue
            card_x = bx + i * BENCH_STEP
            if hit_test(pos, card_x, by - 15, CARD_W, CARD_H + 15):
                game.hovered_card_index = i

def process_mouse_up(game):
    if game.dragging and game.dragged_card_index is not None:
        px, py = ZONES["player_battle"]
        ex, ey = ZONES["enemy_battle"]

        if game.drag_from == "bench" and hit_test(game.drag_pos, px, py):
            old = get_battle_index(game.card_locations)
            if old is not None:
                game.card_locations[old] = "bench"
            game.card_locations[game.dragged_card_index] = "battle"

        elif game.drag_from == "battle" and hit_test(game.drag_pos, ex, ey):
            battle_card = game.player_deck[game.dragged_card_index]
            atks = battle_card.get("attacks", [])
            if atks:
                dmg = get_damage(atks[0])
                game.enemy_hps[game.enemy_index] = do_attack(game.enemy_hps[game.enemy_index], dmg)
                game.enemy_hp = game.enemy_hps[game.enemy_index]
                print(f"{battle_card['name']} attacks! Enemy HP: {game.enemy_hp}")

                if game.enemy_hp == 0:
                    move_to_trash(game.enemy_locations, game.enemy_index)
                    game.enemy_index += 1
                    if game.enemy_index < len(game.enemy_deck):
                        game.enemy_card = game.enemy_deck[game.enemy_index]
                        game.enemy_image = load_card_image(game.enemy_card)
                        game.enemy_hp = game.enemy_hps[game.enemy_index]
                        print(f"New enemy: {game.enemy_card['name']}")
                    else:
                        print("You win!")

            enemy_atks = game.enemy_card.get("attacks", [])
            if enemy_atks:
                enemy_dmg = get_damage(enemy_atks[0])
                game.player_hps[game.dragged_card_index] = do_attack(game.player_hps[game.dragged_card_index], enemy_dmg)
                print(f"{game.enemy_card['name']} attacks back! Player HP: {game.player_hps[game.dragged_card_index]}")
                if game.player_hps[game.dragged_card_index] == 0:
                    move_to_trash(game.card_locations, game.dragged_card_index)
                    print(f"{battle_card['name']} died!")

    game.dragging = False
    game.dragged_card_index = None
    game.drag_from = None