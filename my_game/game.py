import pygame
from config import *
from card_utils import *
from game_logic import *
from trash import *
from render import render as render_game
from events import *
from endscreen import *
from loading_screen import draw_loading
from sound import *

class PokemonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pokemon Card Game")
        self.font = pygame.font.SysFont("Arial", 24)

        draw_loading(self.screen, self.font, "Loading...", 0, 10)
        
        self.background = pygame.image.load("images/background.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_W, SCREEN_H))
        
        
        self.card_back = pygame.image.load("images/cardBack.png")
        self.card_back = pygame.transform.scale(self.card_back, (CARD_W, CARD_H))
        
        
        self.load_cards()
        play_music("sounds/megalovania.mp3")
        self.enemy_locations = ["battle"] + ["bench"] * 4 
        self.card_locations = ["bench"] * 5
        self.player_hps = [int(c.get("hp", 100)) for c in self.player_deck]
        self.enemy_hps = [int(c.get("hp", 100)) for c in self.enemy_deck]
        self.enemy_index = 0
        
        self.player_images = []
        for index, c in enumerate(self.player_deck):
            draw_loading(self.screen, self.font, f"Loading {c['name']}...", index + 1, 10)
            self.player_images.append(load_card_image(c))
            
        self.enemy_images = []
        for index, c in enumerate(self.enemy_deck):
            draw_loading(self.screen, self.font, f"Loading {c['name']}...", index + 6, 10)
            self.enemy_images.append(load_card_image(c))
        
        self.hovered_card_index = None
        self.dragging = False
        self.dragged_card_index = None
        self.drag_pos = (0, 0)
        self.drag_from = None
        self.preview_card = None
        self.preview_image = None
        self.last_click_time = 0
        self.last_click_index = None
        self.enemy_on_field = True
        self.running = True
        self.game_over = False
        self.game_result = None
        self.show_volume_bar = False

    def enemy_card(self):
        if self.enemy_index < len(self.enemy_deck):
            return self.enemy_deck[self.enemy_index]
        return None

    
    def enemy_hp(self):
        if self.enemy_index < len(self.enemy_hps):
            return self.enemy_hps[self.enemy_index]
        return 0

    def load_cards(self):
        all_cards = fetch_cards(limit=10)

        random.shuffle(all_cards)

        self.player_deck = all_cards[:5]
        self.enemy_deck = all_cards[5:]

    def handle_events(self):
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.running = False  
                    else:
                        self.preview_card = None
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
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
