def move_to_trash(card_locations, index):
    card_locations[index] = "trash"

def move_enemy_to_trash(enemy_locations, index):
    enemy_locations[index] = "trash"

def get_trashed(card_locations):
    return [i for i, loc in enumerate(card_locations) if loc == "trash"]

def draw_trash(screen, player_images, card_back, card_locations, enemy_locations, zones):
    # Trash player
    tx, ty = zones["player_trash"]
    trashed = [i for i, loc in enumerate(card_locations) if loc == "trash"]
    if trashed:
        screen.blit(card_back, (tx, ty))
    
    # trash enemy
    etx, ety = zones["enemy_trash"]
    enemy_trashed = [i for i, loc in enumerate(enemy_locations) if loc == "trash"]
    if enemy_trashed:
        screen.blit(card_back, (etx, ety))