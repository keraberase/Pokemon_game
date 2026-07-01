from config import *
from game_logic import *
from card_utils import *
from trash import *
from sound import toggle_mute, set_volume
from attack_menu import get_clicked_attack
from attack_logic import execute_attack


# Handle card click
def handle_card_interaction(game, index, from_zone, pos, now):
    # Double click
    if game.last_click_index == index and now - game.last_click_time < 400:
        game.preview_card = index
        game.preview_image = load_large_image(game.player_bench[index])
    else:
        # Start drag
        game.dragging = True
        game.dragged_card_index = index
        game.drag_from = from_zone
        game.drag_pos = pos
        game.last_click_time = now
        game.last_click_index = index


# Handle mouse down
def process_mouse_down(game, pos, now):
    bx, by = ZONES["player_bench_start"]
    px, py = ZONES["player_battle"]
    ex, ey = ZONES["enemy_battle"]
    cx, cy = SCREEN_W // 2, SCREEN_H // 2

    # Handle attack menu
    if game.attack_menu_open:
        index = get_clicked_attack(pos, game.attack_menu_buttons)
        if index is not None:
            execute_attack(game, index)

        game.attack_menu_open = False
        game.pending_attack_card_index = None
        return

    # Close preview
    if game.preview_card is not None:
        game.preview_card = None
        game.preview_image = None
        return

    # Hide volume bar
    if game.show_volume_bar:
        dx, dy = pos[0] - cx, pos[1] - cy
        on_button = dx * dx + dy * dy <= 40 * 40

        bar_h = 150
        bar_x = cx + 50
        bar_y = cy - bar_h
        on_bar = bar_x < pos[0] < bar_x + 10 and bar_y < pos[1] < bar_y + bar_h

        if not on_button and not on_bar:
            game.show_volume_bar = False

    # Check bench cards
    for i in range(len(game.card_locations)):
        if game.card_locations[i] == "bench" and hit_test(pos, bx + i * game.bench_step, by):
            handle_card_interaction(game, i, "bench", pos, now)
            return

    # Check battle card
    battle_i = get_battle_index(game.card_locations)
    if battle_i is not None and hit_test(pos, px, py):
        handle_card_interaction(game, battle_i, "battle", pos, now)
        return

    # Check enemy card
    if hit_test(pos, ex, ey) and game.enemy_on_field:
        if game.last_click_index == "enemy" and now - game.last_click_time < 400:
            game.preview_card = "enemy"
            game.preview_image = load_large_image(game.enemy_card())
        else:
            game.last_click_time = now
            game.last_click_index = "enemy"

        return

    # Check volume button
    dx, dy = pos[0] - cx, pos[1] - cy
    if dx * dx + dy * dy <= 40 * 40:
        if hasattr(game, "last_vol_click_time") and now - game.last_vol_click_time < 400:
            toggle_mute()
        else:
            game.show_volume_bar = not game.show_volume_bar

        game.last_vol_click_time = now
        return

    # Check log button
    if LOG_X < pos[0] < LOG_X + 60 and LOG_Y < pos[1] < LOG_Y + 20:
        game.show_battle_log = not game.show_battle_log
        return

    # Set volume
    if game.show_volume_bar:
        bar_h = 150
        bar_x = cx + 50
        bar_y = cy - bar_h

        if bar_x < pos[0] < bar_x + 10 and bar_y < pos[1] < bar_y + bar_h:
            clicked_y = pos[1] - bar_y
            new_volume = 1.0 - (clicked_y / bar_h)
            set_volume(max(0.0, min(1.0, new_volume)))
            return


# Handle mouse move
def process_mouse_motion(game, pos):
    # Move dragged card
    if game.dragging:
        game.drag_pos = pos
    else:
        # Check hover
        game.hovered_card_index = None
        bx, by = ZONES["player_bench_start"]

        for i in range(len(game.card_locations)):
            if game.card_locations[i] != "bench":
                continue

            card_x = bx + i * game.bench_step
            if hit_test(pos, card_x, by - 15, CARD_W, CARD_H + 15):
                game.hovered_card_index = i


# Handle mouse up
def process_mouse_up(game):
    if game.dragging and game.dragged_card_index is not None:
        px, py = ZONES["player_battle"]
        ex, ey = ZONES["enemy_battle"]

        # Move to battle
        if game.drag_from == "bench" and hit_test(game.drag_pos, px, py):
            old = get_battle_index(game.card_locations)

            if old is not None:
                game.card_locations[old] = "bench"

            game.card_locations[game.dragged_card_index] = "battle"

        # Start attack
        elif game.drag_from == "battle" and hit_test(game.drag_pos, ex, ey) and game.enemy_on_field:
            game.attack_menu_open = True
            game.pending_attack_card_index = game.dragged_card_index
            game.dragging = False
            game.dragged_card_index = None
            game.drag_from = None
            return

    # Stop drag
    game.dragging = False
    game.dragged_card_index = None
    game.drag_from = None


# Handle mouse wheel
def process_mouse_wheel(game, y):
    if game.show_battle_log:
        game.log_scroll = max(0, min(
            max(0, len(game.battle_log) - MAX_LOGS),
            game.log_scroll - y
        ))