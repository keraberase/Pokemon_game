# Move card
def move_to_trash(card_locations, index):
    card_locations[index] = "trash"


# Draw trash piles
def draw_trash(screen, card_back, card_locations, enemy_locations, zones, player_trash_count=0, enemy_trash_count=0):
    
    if "trash" in card_locations or player_trash_count > 0:
        screen.blit(card_back, zones["player_trash"])

    
    if "trash" in enemy_locations or enemy_trash_count > 0:
        screen.blit(card_back, zones["enemy_trash"])