import pygame
from config import *
from card_utils import load_card_image, load_large_image, fetch_cards
from game_logic import get_damage, do_attack, get_battle_index, hit_test, draw_text

class PokemonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pokemon Card Game")
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Load background
        self.background = pygame.image.load("images/background.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_W, SCREEN_H))
        
        # Load card back
        self.card_back = pygame.image.load("images/cardBack.png")
        self.card_back = pygame.transform.scale(self.card_back, (CARD_W, CARD_H))
        
        # Fetch cards using the new utility function
        self.load_cards()
        
        # Game State
        self.card_locations = ["bench"] * 5
        self.player_hps = [int(c.get("hp", 100)) for c in self.player_deck]
        self.enemy_hps = [int(c.get("hp", 100)) for c in self.enemy_deck]
        self.enemy_index = 0
        self.enemy_card = self.enemy_deck[self.enemy_index]
        self.enemy_hp = self.enemy_hps[self.enemy_index]
        
        # Load images
        self.player_images = [load_card_image(c) for c in self.player_deck]
        self.enemy_image = load_card_image(self.enemy_card)
        
        # UI State
        self.hovered_card_index = None
        self.dragging = False
        self.dragged_card_index = None
        self.drag_pos = (0, 0)
        self.drag_from = None
        self.preview_card = None
        self.preview_image = None
        self.last_click_time = 0
        self.last_click_index = None
        
        self.running = True

    def load_cards(self):
        all_cards = fetch_cards(limit=10)
        self.player_deck = all_cards[:5]
        self.enemy_deck = all_cards[5:]

    def handle_double_click(self, index, card, now):
        self.preview_card = card
        self.preview_image = load_large_image(card)
        
    def handle_events(self):
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.preview_card = None
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.process_mouse_down(event.pos, now)
                
            elif event.type == pygame.MOUSEMOTION:
                self.process_mouse_motion(event.pos)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                self.process_mouse_up()

    def process_mouse_down(self, pos, now):
        bx, by = ZONES["player_bench_start"]
        px, py = ZONES["player_battle"]
        ex, ey = ZONES["enemy_battle"]
        
        # Check bench cards
        for i in range(5):
            if self.card_locations[i] != "bench":
                continue
            card_x = bx + i * BENCH_STEP
            if hit_test(pos, card_x, by):
                if self.last_click_index == i and now - self.last_click_time < 400:
                    self.handle_double_click(i, self.player_deck[i], now)
                else:
                    self.dragging = True
                    self.dragged_card_index = i
                    self.drag_from = "bench"
                    self.drag_pos = pos
                    self.last_click_time = now
                    self.last_click_index = i
                return

        # Check player battle card
        battle_i = get_battle_index(self.card_locations)
        if battle_i is not None and hit_test(pos, px, py):
            if self.last_click_index == battle_i and now - self.last_click_time < 400:
                self.handle_double_click(battle_i, self.player_deck[battle_i], now)
            else:
                self.dragging = True
                self.dragged_card_index = battle_i
                self.drag_from = "battle"
                self.drag_pos = pos
                self.last_click_time = now
                self.last_click_index = battle_i
            return

        # Check enemy battle card
        if hit_test(pos, ex, ey):
            self.handle_double_click("enemy", self.enemy_card, now)

    def process_mouse_motion(self, pos):
        if self.dragging:
            self.drag_pos = pos
        else:
            self.hovered_card_index = None
            bx, by = ZONES["player_bench_start"]
            for i in range(5):
                if self.card_locations[i] != "bench":
                    continue
                card_x = bx + i * BENCH_STEP
                if card_x < pos[0] < card_x + 90 and by - 15 < pos[1] < by + 102:
                    self.hovered_card_index = i

    def process_mouse_up(self):
        if self.dragging and self.dragged_card_index is not None:
            px, py = ZONES["player_battle"]
            ex, ey = ZONES["enemy_battle"]
            
            # Place to battle field
            if self.drag_from == "bench" and hit_test(self.drag_pos, px, py):
                old_battle = get_battle_index(self.card_locations)
                if old_battle is not None:
                    self.card_locations[old_battle] = "bench"
                self.card_locations[self.dragged_card_index] = "battle"
                
            # Attack enemy
            elif self.drag_from == "battle" and hit_test(self.drag_pos, ex, ey):
                battle_card = self.player_deck[self.dragged_card_index]
                atks = battle_card.get("attacks", [])
                if atks:
                    dmg = get_damage(atks[0])
                    self.enemy_hps[self.enemy_index] = do_attack(self.enemy_hps[self.enemy_index], dmg)
                    self.enemy_hp = self.enemy_hps[self.enemy_index]
                    print(f"{battle_card['name']} attacks! Enemy HP: {self.enemy_hp}")
                    
                    if self.enemy_hp == 0:
                        self.enemy_index += 1
                        
                    if self.enemy_index < len(self.enemy_deck):
                        self.enemy_card = self.enemy_deck[self.enemy_index]
                        self.enemy_image = load_card_image(self.enemy_card)
                        self.enemy_hp = self.enemy_hps[self.enemy_index]
                        print(f"New enemy: {self.enemy_card['name']}")
                    else:
                        print("You win!")
                
                # Enemy counter-attack
                enemy_atks = self.enemy_card.get("attacks", [])
                if enemy_atks:
                    enemy_dmg = get_damage(enemy_atks[0])
                    self.player_hps[self.dragged_card_index] = do_attack(self.player_hps[self.dragged_card_index], enemy_dmg)
                    print(f"{self.enemy_card['name']} attacks back! Player HP: {self.player_hps[self.dragged_card_index]}")

        self.dragging = False
        self.dragged_card_index = None
        self.drag_from = None

    def render(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw enemy battle card and HP
        ex, ey = ZONES["enemy_battle"]
        draw_text(self.screen, self.font, f"HP: {self.enemy_hp}", (ex, ey - 25))
        self.screen.blit(self.enemy_image, (ex, ey))
        
        # Draw player battle card and HP
        px, py = ZONES["player_battle"]
        battle_i = get_battle_index(self.card_locations)
        if battle_i is not None:
            self.screen.blit(self.player_images[battle_i], (px, py))
            draw_text(self.screen, self.font, f"HP: {self.player_hps[battle_i]}", (px, py - 25))
            
        # Draw player bench cards
        bx, by = ZONES["player_bench_start"]
        for i, image in enumerate(self.player_images):
            if self.card_locations[i] != "bench":
                continue
            if i == self.dragged_card_index and self.dragging:
                continue
            offset_y = -15 if self.hovered_card_index == i else 0
            self.screen.blit(image, (bx + i * BENCH_STEP, by + offset_y))
            
        # Draw enemy bench cards
        ebx, eby = ZONES["enemy_bench_start"]
        for i in range(4):
            self.screen.blit(self.card_back, (ebx + i * BENCH_STEP, eby))
            
        # Draw dragged card
        if self.dragging and self.dragged_card_index is not None:
            self.screen.blit(self.player_images[self.dragged_card_index], (self.drag_pos[0] - 45, self.drag_pos[1] - 51))
            
        # Draw card preview
        if self.preview_card is not None and self.preview_image is not None:
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(self.preview_image, (275, 125))
            draw_text(self.screen, self.font, "ESC - close", (310, 490), (200, 200, 200))
            
        # Draw coordinates
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.font.render(f"X:{mouse_pos[0]} Y:{mouse_pos[1]}", True, (255, 255, 0)), (10, 10))
        
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.render()
            clock.tick(60)
        pygame.quit()
