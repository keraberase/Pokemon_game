import requests
import pygame
from config import *
from card_utils import *
from game_logic import *


pygame.init()

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (SCREEN_W, SCREEN_H))
pygame.display.set_caption("Pokemon Card Game")
font = pygame.font.SysFont("Arial", 24)

import requests
response = requests.get("https://api.pokemontcg.io/v2/cards", params={"pageSize": 10})
if response.status_code != 200:
    print("Error API:", response.status_code)
    exit()
all_cards = response.json()["data"]
player_deck = all_cards[:5]
enemy_deck = all_cards[5:]
enemy_card = enemy_deck[0]

player_hp = int(player_deck[0].get("hp", 100))
enemy_hp = int(enemy_card.get("hp", 100))

card_locations = ["bench"] * 5
player_hps = [int(c.get("hp", 100)) for c in player_deck]
enemy_hps = [int(c.get("hp", 100)) for c in enemy_deck]
enemy_hp = enemy_hps[0]
enemy_index = 0
hovered_card_index = None
dragging = False
dragged_card_index = None
drag_pos = (0, 0)
drag_from = None
preview_card = None
preview_image = None
last_click_time = 0
last_click_index = None

player_images = [load_card_image(c) for c in player_deck]
enemy_image = load_card_image(enemy_card)
card_back = pygame.image.load("images/cardBack.png")
card_back = pygame.transform.scale(card_back, (CARD_W, CARD_H))

preview_card = None   
preview_image = None  
last_click_time = 0
last_click_index = None





running = True
font = pygame.font.SysFont("Arial", 24)

while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                preview_card = None    

        if event.type == pygame.MOUSEBUTTONDOWN:
            bx, by = ZONES["player_bench_start"]
            px, py = ZONES["player_battle"]
            ex, ey = ZONES["enemy_battle"]

            for i in range(5):
                if card_locations[i] != "bench":
                    continue
                card_x = bx + i * BENCH_STEP
                if hit_test(event.pos, card_x, by):
                    if last_click_index == i and now - last_click_time < 400:
                        handle_double_click(i, player_deck[i], now)
                    else:
                        dragging = True
                        dragged_card_index = i
                        drag_from = "bench"
                        drag_pos = event.pos
                        last_click_time = now
                        last_click_index = i

            battle_i = get_battle_index(card_locations)
            if battle_i is not None and hit_test(event.pos, px, py):
                if last_click_index == battle_i and now - last_click_time < 400:
                    handle_double_click(battle_i, player_deck[battle_i], now)
                else:
                    dragging = True
                    dragged_card_index = battle_i
                    drag_from = "battle"
                    drag_pos = event.pos
                    last_click_time = now
                    last_click_index = battle_i

            if hit_test(event.pos, ex, ey):
                handle_double_click("enemy", enemy_card, now)

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                drag_pos = event.pos
            else:
                hovered_card_index = None
                bx, by = ZONES["player_bench_start"]
                for i in range(5):
                    if card_locations[i] != "bench":
                        continue
                    card_x = bx + i * BENCH_STEP
                    if card_x < event.pos[0] < card_x + 90 and by - 15 < event.pos[1] < by + 102:
                        hovered_card_index = i

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging and dragged_card_index is not None:
                px, py = ZONES["player_battle"]
                ex, ey = ZONES["enemy_battle"]

                
                if drag_from == "bench" and hit_test(drag_pos, px, py):
                    old_battle = get_battle_index(card_locations)
                    if old_battle is not None:
                        card_locations[old_battle] = "bench"
                    card_locations[dragged_card_index] = "battle"
                    
                    

                # attack enemey
                elif drag_from == "battle" and hit_test(drag_pos, ex, ey):
                    battle_card = player_deck[dragged_card_index]
                    atks = battle_card.get("attacks", [])
                    if atks:
                        dmg = get_damage(atks[0])
                        enemy_hps[enemy_index] = do_attack(enemy_hps[enemy_index], dmg)
                        enemy_hp = enemy_hps[enemy_index]
                        print(f"{battle_card['name']} attacks! Enemy HP: {enemy_hp}")
                        
                        if enemy_hp == 0:
                            enemy_index += 1
                        if enemy_index < len(enemy_deck):
                            enemy_card = enemy_deck[enemy_index]
                            enemy_image = load_card_image(enemy_card)
                            enemy_hp = enemy_hps[enemy_index]
                            print(f"New enemy: {enemy_card['name']}")
                        else:
                            print("You win!")
                        

                    enemy_atks = enemy_card.get("attacks", [])
                    if enemy_atks:
                        enemy_dmg = get_damage(enemy_atks[0])
                        player_hps[dragged_card_index] = do_attack(player_hps[dragged_card_index], enemy_dmg)
                        print(f"{enemy_card['name']} attacks back! Player HP: {player_hps[dragged_card_index]}")

            dragging = False
            dragged_card_index = None
            drag_from = None

    screen.blit(background, (0, 0))
    font = pygame.font.SysFont("Arial", 24)

    ex, ey = ZONES["enemy_battle"]
    draw_text(font, f"HP: {enemy_hp}", (ex, ey - 25))
    screen.blit(enemy_image, (ex, ey))

    px, py = ZONES["player_battle"]
    battle_i = get_battle_index(card_locations)
    if battle_i is not None:
        screen.blit(player_images[battle_i], (px, py))
        draw_text(font, f"HP: {player_hps[battle_i]}", (px, py - 25))

    # brench player
    bx, by = ZONES["player_bench_start"]
    for i, image in enumerate(player_images):
        if card_locations[i] != "bench":
            continue
        if i == dragged_card_index and dragging:
            continue
        offset_y = -15 if hovered_card_index == i else 0
        screen.blit(image, (bx + i * BENCH_STEP, by + offset_y))

   
    # enemy card
    ebx, eby = ZONES["enemy_bench_start"]
    for i in range(4):
        screen.blit(card_back, (ebx + i * BENCH_STEP, eby))

    # drag card
    if dragging and dragged_card_index is not None:
        screen.blit(player_images[dragged_card_index], (drag_pos[0] - 45, drag_pos[1] - 51))

    if preview_card is not None and preview_image is not None:
       
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        screen.blit(preview_image, (275, 125))
        draw_text(font, "ESC - close", (310, 490), (200, 200, 200))

    mouse_pos = pygame.mouse.get_pos()
    screen.blit(font.render(f"X:{mouse_pos[0]} Y:{mouse_pos[1]}", True, (255, 255, 0)), (10, 10))

    pygame.display.flip()

pygame.quit()