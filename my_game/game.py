import pygame
from config import *
from card_utils import *
from game_logic import *
from trash import *
from render import render as render_game
from events import *
from endscreen import *
from loading_screen import draw_loading
from start_menu import *
from video_intro import *
from sound import *
import random
from attack_logic import *


class PokemonGame:
    # Menu delay
    MENU_APPEAR_DELAY_MS = 2000

    def __init__(self):
        # Init pygame
        pygame.init()

        # Create window
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pokemon Card Game")
        self.font = pygame.font.SysFont("Arial", 24)

        # Load background
        self.background = pygame.image.load("images/background.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_W, SCREEN_H))

        # Load card back
        self.card_back = pygame.image.load("images/cardBack.png")
        self.card_back = pygame.transform.scale(self.card_back, (CARD_W, CARD_H))

        # Play menu music
        play_music("sounds/menu_theme.mp3")

        # Load intro video
        self.video = VideoIntro("videos/intro.mp4")
        self.state = "menu"

        # Setup menu overlay
        if self.video.available:
            self.menu_appear_time = pygame.time.get_ticks() + self.MENU_APPEAR_DELAY_MS
            self.show_menu_overlay = False
        else:
            self.menu_appear_time = 0
            self.show_menu_overlay = True

        # Menu state
        self.selected_total = 10
        self.menu_buttons = []
        self.menu_start_button = None
        self.bench_step = BENCH_STEP

        # Game state
        self.running = True
        self.game_over = False
        self.game_result = None

    # Handle menu input
    def handle_menu_events(self):
        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                self.running = False

            # Exit menu
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            # Show menu early
            elif not self.show_menu_overlay and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.show_menu_overlay = True

            # Handle menu click
            elif self.show_menu_overlay and event.type == pygame.MOUSEBUTTONDOWN:
                clicked_total = get_clicked_total(event.pos, self.menu_buttons)

                if clicked_total is not None:
                    self.selected_total = clicked_total
                elif is_start_clicked(event.pos, self.menu_start_button):
                    self.start_game(self.selected_total)

    # Draw menu
    def render_menu(self):
        # Draw video
        if self.video.available:
            self.video.update()
            self.video.draw(self.screen)
        else:
            self.screen.fill((20, 20, 20))

        # Show menu
        if not self.show_menu_overlay and pygame.time.get_ticks() >= self.menu_appear_time:
            self.show_menu_overlay = True

        # Draw overlay
        if self.show_menu_overlay:
            self.menu_buttons, self.menu_start_button = draw_start_menu(
                self.screen,
                self.font,
                self.selected_total,
                overlay=self.video.available
            )
        else:
            self.menu_buttons, self.menu_start_button = [], None
            pygame.display.flip()

    # Start game
    def start_game(self, total_count):
        # Save settings
        self.total_count = total_count
        self.bench_step = BENCH_STEP

        # Play game music
        play_music("sounds/megalovania.mp3")

        # Show loading
        draw_loading(self.screen, self.font, "Loading...", 0, 1)

        # Load card data
        if not self.load_cards(total_count):
            return

        # Player cards
        self.card_locations = ["bench"] * BENCH_SIZE
        self.player_hps = [int(c.get("hp", 100)) for c in self.player_bench]
        self.player_deck_hps = [int(c.get("hp", 100)) for c in self.player_deck_pile]

        # Enemy cards
        self.enemy_locations = ["battle"] + ["bench"] * (BENCH_SIZE - 1)
        self.enemy_index = 0
        self.enemy_hps = [int(c.get("hp", 100)) for c in self.enemy_bench]
        self.enemy_deck_hps = [int(c.get("hp", 100)) for c in self.enemy_deck_pile]

        # Count images
        total_images = (
            len(self.player_bench)
            + len(self.player_deck_pile)
            + len(self.enemy_bench)
            + len(self.enemy_deck_pile)
        )

        loaded_images = 0

        # Load player bench
        self.player_images = []
        for c in self.player_bench:
            loaded_images += 1
            draw_loading(self.screen, self.font, f"Loading {c['name']}...", loaded_images, total_images)
            self.player_images.append(load_card_image(c))

        # Load player deck
        self.player_deck_images = []
        for c in self.player_deck_pile:
            loaded_images += 1
            draw_loading(self.screen, self.font, f"Loading {c['name']}...", loaded_images, total_images)
            self.player_deck_images.append(load_card_image(c))

        # Load enemy bench
        self.enemy_images = []
        for c in self.enemy_bench:
            loaded_images += 1
            draw_loading(self.screen, self.font, f"Loading {c['name']}...", loaded_images, total_images)
            self.enemy_images.append(load_card_image(c))

        # Load enemy deck
        self.enemy_deck_images = []
        for c in self.enemy_deck_pile:
            loaded_images += 1
            draw_loading(self.screen, self.font, f"Loading {c['name']}...", loaded_images, total_images)
            self.enemy_deck_images.append(load_card_image(c))

        # Battle log
        self.battle_log = []
        self.show_battle_log = True
        self.log_scroll = 0

        # Mouse state
        self.hovered_card_index = None
        self.dragging = False
        self.dragged_card_index = None
        self.drag_pos = (0, 0)
        self.drag_from = None

        # Preview state
        self.preview_card = None
        self.preview_image = None
        self.last_click_time = 0
        self.last_click_index = None

        # Match state
        self.enemy_on_field = True
        self.game_over = False
        self.game_result = None

        # UI state
        self.show_volume_bar = False
        self.attack_menu_open = False
        self.attack_menu_buttons = []
        self.pending_attack_card_index = None

        # Trash counts
        self.player_trash_count = 0
        self.enemy_trash_count = 0

        # Enemy spawn
        self.enemy_spawn_time = 0
        self.enemy_waiting_spawn = False

        # Enter game
        self.state = "playing"

    # Get enemy card
    def enemy_card(self):
        if self.enemy_index < len(self.enemy_bench):
            return self.enemy_bench[self.enemy_index]
        return None

    # Get enemy HP
    def enemy_hp(self):
        if self.enemy_index < len(self.enemy_hps):
            return self.enemy_hps[self.enemy_index]
        return 0

    # Load cards
    def load_cards(self, total_count):
        # Needed cards
        needed = total_count * 2
        all_cards = fetch_cards(limit=needed)

        # Retry loading
        attempts = 0
        while len(all_cards) < needed and attempts < 3:
            attempts += 1
            all_cards = fetch_cards(limit=needed)

        # Handle failure
        if len(all_cards) < needed:
            draw_loading(
                self.screen,
                self.font,
                "Couldn't fetch enough cards. Try a smaller number or check your connection.",
                0,
                1
            )
            pygame.time.wait(3000)
            self.running = False
            return False

        # Split cards
        random.shuffle(all_cards)
        self.player_bench = all_cards[:BENCH_SIZE]
        self.player_deck_pile = all_cards[BENCH_SIZE:total_count]
        self.enemy_bench = all_cards[total_count:total_count + BENCH_SIZE]
        self.enemy_deck_pile = all_cards[total_count + BENCH_SIZE:total_count * 2]

        return True

    # Handle game input
    def handle_events(self):
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                self.running = False

            # Keyboard input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.running = False
                    else:
                        self.preview_card = None

                # Restart game
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
                    self.show_menu_overlay = True

            # Mouse down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                process_mouse_down(self, event.pos, now)

            # Mouse wheel
            elif event.type == pygame.MOUSEWHEEL:
                process_mouse_wheel(self, event.y)

            # Mouse move
            elif event.type == pygame.MOUSEMOTION:
                process_mouse_motion(self, event.pos)

            # Mouse up
            elif event.type == pygame.MOUSEBUTTONUP:
                process_mouse_up(self)

    # Draw game
    def render(self):
        render_game(self)

    # Main loop
    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            # Menu loop
            if self.state == "menu":
                self.handle_menu_events()
                self.render_menu()

            # Game loop
            else:
                self.handle_events()
                update_enemy_spawn(self)
                self.render()

            # Limit FPS
            clock.tick(60)

        # Close pygame
        pygame.quit()