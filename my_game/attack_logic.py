import pygame
from game_logic import *
from trash import *
from card_utils import *


# Execute attack
def execute_attack(game, attack_index):
    # Get cards
    battle_card = game.player_bench[game.pending_attack_card_index]
    enemy_card = game.enemy_card()
    enemy_index = game.enemy_index
    atks = battle_card.get("attacks", [])

    # Check attack
    if not atks or attack_index >= len(atks):
        return

    # Damage enemy
    dmg = get_damage(atks[attack_index])
    game.enemy_hps[enemy_index] = max(0, game.enemy_hps[enemy_index] - dmg)
    add_log(game, f"{battle_card['name']}: -{dmg} HP")

    # Check enemy
    enemy_died = game.enemy_hps[enemy_index] == 0

    # Enemy turn
    if not enemy_died:
        enemy_attack(game, battle_card, enemy_card)
        return

    # Enemy died
    add_log(game, f"{enemy_card['name']} died!")
    move_to_trash(game.enemy_locations, enemy_index)
    game.enemy_trash_count += 1
    game.enemy_index += 1
    game.enemy_on_field = False

    # Next enemy
    if game.enemy_index < len(game.enemy_bench):
        game.enemy_locations[game.enemy_index] = "battle"
        game.enemy_on_field = True
        start_enemy_bench_spawn(game)

    # Draw enemy
    elif game.enemy_deck_pile:
        draw_enemy_from_deck(game, "battle")
        game.enemy_on_field = True

    # Player wins
    else:
        game.game_over = True
        game.game_result = "win"


# Update enemy spawn
def update_enemy_spawn(game):
    if game.enemy_waiting_spawn and pygame.time.get_ticks() >= game.enemy_spawn_time:
        game.enemy_waiting_spawn = False
        draw_enemy_from_deck(game, "bench")


# Enemy attack
def enemy_attack(game, battle_card, enemy_card=None):
    # Get enemy
    if enemy_card is None:
        if not game.enemy_on_field:
            return
        enemy_card = game.enemy_card()

    # Get attacks
    enemy_atks = enemy_card.get("attacks", [])
    if not enemy_atks:
        return

    # Damage player
    index = game.pending_attack_card_index
    enemy_dmg = get_damage(max(enemy_atks, key=lambda a: get_damage(a)))
    game.player_hps[index] = max(0, game.player_hps[index] - enemy_dmg)
    add_log(game, f"{enemy_card['name']}: -{enemy_dmg} HP")

    # Check player
    if game.player_hps[index] != 0:
        return

    # Player died
    move_to_trash(game.card_locations, index)
    game.player_trash_count += 1
    add_log(game, f"Your {battle_card['name']} died!")

    # Draw player
    if game.player_deck_pile:
        new_card, new_image = game.player_deck_pile.pop(), game.player_deck_images.pop()
        game.player_bench[index] = new_card
        game.player_hps[index] = int(new_card.get("hp", 100))
        game.player_images[index] = new_image
        game.card_locations[index] = "bench"
        add_log(game, f"{new_card['name']} joins from deck!")

    # Player loses
    if all(loc == "trash" for loc in game.card_locations):
        game.game_over = True
        game.game_result = "lose"


# Start enemy spawn
def start_enemy_bench_spawn(game):
    if game.enemy_deck_pile:
        game.enemy_waiting_spawn = True
        game.enemy_spawn_time = pygame.time.get_ticks() + 1000


# Draw enemy card
def draw_enemy_from_deck(game, location):
    # Check deck
    if not game.enemy_deck_pile:
        return

    # Move card
    new_card, new_image = game.enemy_deck_pile.pop(), game.enemy_deck_images.pop()
    game.enemy_bench.append(new_card)
    game.enemy_hps.append(int(new_card.get("hp", 100)))
    game.enemy_images.append(new_image)
    game.enemy_locations.append(location)

    # Log card
    add_log(game, f"Enemy {new_card['name']} joins from deck!")