import pygame
from config import *
from card_utils import *
from game_logic import *
from trash import *
from render import render as render_game
from events import *

class PokemonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pokemon Card Game")
        self.font = pygame.font.SysFont("Arial", 24)
        
        
        self.background = pygame.image.load("images/background.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_W, SCREEN_H))
        
        
        self.card_back = pygame.image.load("images/cardBack.png")
        self.card_back = pygame.transform.scale(self.card_back, (CARD_W, CARD_H))
        
        
        self.load_cards()
        
        self.enemy_locations = ["bench"] * 5
        self.card_locations = ["bench"] * 5
        self.player_hps = [int(c.get("hp", 100)) for c in self.player_deck]
        self.enemy_hps = [int(c.get("hp", 100)) for c in self.enemy_deck]
        self.enemy_index = 0
        self.enemy_card = self.enemy_deck[self.enemy_index]
        self.enemy_hp = self.enemy_hps[self.enemy_index]
        
        
        self.player_images = [load_card_image(c) for c in self.player_deck]
        self.enemy_image = load_card_image(self.enemy_card)
        
        
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
                process_mouse_down(self, event.pos, now)
            elif event.type == pygame.MOUSEMOTION:
                process_mouse_motion(self, event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                process_mouse_up(self)

    
    def render(self):
        render_game(self)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.render()
            clock.tick(60)
        pygame.quit()
