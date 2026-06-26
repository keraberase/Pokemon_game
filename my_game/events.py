from config import *
from game_logic import *
from card_utils import *
from trash import *
from sound import toggle_mute, set_volume

def handle_card_interaction(game, index, from_zone, pos, now):
    if game.last_click_index == index and now - game.last_click_time < 400:
        game.preview_card = index
        game.preview_image = load_large_image(game.player_deck[index])
    else:
        game.dragging = True
        game.dragged_card_index = index
        game.drag_from = from_zone
        game.drag_pos = pos
        game.last_click_time = now
        game.last_click_index = index

def process_mouse_down(game, pos, now):
    bx, by = ZONES["player_bench_start"]
    px, py = ZONES["player_battle"]
    ex, ey = ZONES["enemy_battle"]
    cx, cy = SCREEN_W // 2, SCREEN_H // 2

    # close preview card on any click
    if game.preview_card is not None:
        game.preview_card = None
        game.preview_image = None
        return

    # auto-close volume bar
    if game.show_volume_bar:
        dx, dy = pos[0] - cx, pos[1] - cy
        on_button = dx*dx + dy*dy <= 40*40
        bar_h = 150
        bar_x = cx + 50
        bar_y = cy - bar_h
        on_bar = bar_x < pos[0] < bar_x + 10 and bar_y < pos[1] < bar_y + bar_h
        
        if not on_button and not on_bar:
            game.show_volume_bar = False

    # player bench
    for i in range(5):
        if game.card_locations[i] == "bench" and hit_test(pos, bx + i * BENCH_STEP, by):
            handle_card_interaction(game, i, "bench", pos, now)
            return

    # active battle card
    battle_i = get_battle_index(game.card_locations)
    if battle_i is not None and hit_test(pos, px, py):
        handle_card_interaction(game, battle_i, "battle", pos, now)
        return

    # enemy preview
    if hit_test(pos, ex, ey) and game.enemy_on_field:
        if game.last_click_index == "enemy" and now - game.last_click_time < 400:
            game.preview_card = "enemy"
            game.preview_image = load_large_image(game.enemy_card)
        game.last_click_time = now
        game.last_click_index = "enemy"
    
    # volume button click
    dx, dy = pos[0] - cx, pos[1] - cy
    if dx*dx + dy*dy <= 40*40:
        if hasattr(game, "last_vol_click_time") and now - game.last_vol_click_time < 400:
            toggle_mute()
        else:
            game.show_volume_bar = not game.show_volume_bar
        game.last_vol_click_time = now
        return

    # volume bar adjustment
    if game.show_volume_bar:
        bar_h = 150
        bar_x = cx + 50
        bar_y = cy - bar_h
        if bar_x < pos[0] < bar_x + 10 and bar_y < pos[1] < bar_y + bar_h:
            clicked_y = pos[1] - bar_y
            new_volume = 1.0 - (clicked_y / bar_h)
            set_volume(max(0.0, min(1.0, new_volume)))
            return

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

        elif game.drag_from == "battle" and hit_test(game.drag_pos, ex, ey) and game.enemy_on_field:
            battle_card = game.player_deck[game.dragged_card_index]
            atks = battle_card.get("attacks", [])
            if atks:
                dmg = get_damage(atks[0])
                game.enemy_hps[game.enemy_index] = do_attack(game.enemy_hps[game.enemy_index], dmg)
                print(f"{battle_card['name']} attacks! Enemy HP: {game.enemy_hp}")

            if game.enemy_hp == 0:
                move_to_trash(game.enemy_locations, game.enemy_index)
                game.enemy_index += 1
                game.enemy_on_field = False
                
                if game.enemy_index < len(game.enemy_deck):
                    game.enemy_locations[game.enemy_index] = "battle"
                    game.enemy_on_field = True
                else:
                    game.game_over = True
                    game.game_result = "win"

            # enemy attacks back
            if not game.game_over and game.enemy_on_field:
                enemy_atks = game.enemy_card.get("attacks", [])
                if enemy_atks:
                    enemy_dmg = get_damage(enemy_atks[0])
                    game.player_hps[game.dragged_card_index] = do_attack(game.player_hps[game.dragged_card_index], enemy_dmg)
                    print(f"{game.enemy_card['name']} attacks back! Player HP: {game.player_hps[game.dragged_card_index]}")
                    if game.player_hps[game.dragged_card_index] == 0:
                        move_to_trash(game.card_locations, game.dragged_card_index)
                        print(f"{battle_card['name']} died!")

            # check defeat
            if all(loc == "trash" for loc in game.card_locations):
                game.game_over = True
                game.game_result = "lose"

    game.dragging = False
    game.dragged_card_index = None
    game.drag_from = None