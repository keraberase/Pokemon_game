def move_to_trash(card_locations, index):
    card_locations[index] = "trash"

def draw_trash(screen, card_back, card_locations, enemy_locations, zones):
    # trash player
    if "trash" in card_locations:
        screen.blit(card_back, zones["player_trash"])
    
    # trash enemy
    if "trash" in enemy_locations:
        screen.blit(card_back, zones["enemy_trash"])