from config import CARD_W, CARD_H


def get_damage(atk):
    digits = ''.join(filter(str.isdigit, atk.get("damage", "")))
    return int(digits) if digits else 10

def do_attack(defender_hp, damage):
    return max(0, defender_hp - damage)

def get_battle_index(card_locations):
    return next((i for i in range(5) if card_locations[i] == "battle"), None)

def hit_test(pos, x, y, w=CARD_W, h=CARD_H):
    return x < pos[0] < x + w and y < pos[1] < y + h

# def draw_text(font, text, pos, color=(255, 255, 255)):
#     screen.blit(font.render(text, True, color), pos)