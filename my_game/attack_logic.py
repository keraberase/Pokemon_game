
from game_logic import *
from trash import *

def execute_attack(game, attack_index):
    battle_card = game.player_deck[game.pending_attack_card_index]
    atks = battle_card.get("attacks", [])
    
    if not atks or attack_index >= len(atks):
        return

    dmg = get_damage(atks[attack_index])
    game.enemy_hps[game.enemy_index] = max(0, game.enemy_hps[game.enemy_index] - dmg)
    add_log(game, f"{battle_card['name']}: -{dmg} HP")

    
    if game.enemy_hp() == 0:
        move_to_trash(game.enemy_locations, game.enemy_index)
        game.enemy_index += 1
        game.enemy_on_field = False
        if game.enemy_index < len(game.enemy_deck):
            game.enemy_locations[game.enemy_index] = "battle"
            game.enemy_on_field = True
        else:
            game.game_over = True
            game.game_result = "win"
            return

    
    if game.enemy_on_field:
        enemy_atks = game.enemy_card().get("attacks", [])
        if enemy_atks:
            enemy_dmg = get_damage(enemy_atks[0])
            idx = game.pending_attack_card_index
            game.player_hps[idx] = max(0, game.player_hps[idx] - enemy_dmg)
            add_log(game, f"{game.enemy_card()['name']}: -{enemy_dmg} HP")
            if game.player_hps[idx] == 0:
                move_to_trash(game.card_locations, idx)
                print(f"{battle_card['name']} died!")

    if all(loc == "trash" for loc in game.card_locations):
        game.game_over = True
        game.game_result = "lose"