import pygame
from config import SCREEN_W, SCREEN_H

# Try Pillow
try:
    from PIL import Image, ImageSequence
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# Animation data
_pikachu_frames = []
_pikachu_frame_delay = 50


# Load Pikachu GIF
def _load_pikachu_frames():
    global _pikachu_frames

    # Skip reload
    if _pikachu_frames:
        return

    # Check Pillow
    if not PIL_AVAILABLE:
        return

    try:
        # Open GIF
        gif = Image.open("images/pikachu_run.gif")

        # Read frames
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")

            # Get background
            bg_color = frame.getpixel((0, 0))
            pixels = frame.load()

            # Remove background
            for y in range(frame.height):
                for x in range(frame.width):
                    if pixels[x, y][:3] == bg_color[:3]:
                        pixels[x, y] = (0, 0, 0, 0)

            # Make surface
            surface = pygame.image.fromstring(
                frame.tobytes(),
                frame.size,
                frame.mode
            ).convert_alpha()

            # Scale Pikachu
            surface = pygame.transform.scale(surface, (70, 50))
            _pikachu_frames.append(surface)

    except Exception:
        # Use fallback
        _pikachu_frames = []


# Draw loading screen
def draw_loading(screen, font, message="Loading...", progress=0, total=1):
    # Clear screen
    screen.fill((20, 20, 20))

    # Load animation
    _load_pikachu_frames()

    # Draw text
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, ((SCREEN_W - text.get_width()) // 2, SCREEN_H // 2 - 80))

    # Bar layout
    bar_w = 460
    bar_h = 24
    bar_x = (SCREEN_W - bar_w) // 2
    bar_y = SCREEN_H // 2

    # Get progress
    progress_ratio = progress / total if total else 0
    progress_ratio = max(0, min(1, progress_ratio))
    fill_w = int(bar_w * progress_ratio)

    # Draw bar
    pygame.draw.rect(
        screen,
        (45, 45, 45),
        (bar_x, bar_y, bar_w, bar_h),
        border_radius=12
    )

    # Fill bar
    if fill_w > 0:
        pygame.draw.rect(
            screen,
            (255, 204, 0),
            (bar_x, bar_y, fill_w, bar_h),
            border_radius=12
        )

    # Draw border
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (bar_x, bar_y, bar_w, bar_h),
        2,
        border_radius=12
    )

    # Draw Pikachu
    if _pikachu_frames and fill_w > 0:
        frame_index = (pygame.time.get_ticks() // _pikachu_frame_delay) % len(_pikachu_frames)
        pikachu = _pikachu_frames[frame_index]

        # Set position
        pika_x = bar_x + fill_w - pikachu.get_width() // 2
        pika_y = bar_y + bar_h // 2 - pikachu.get_height() // 2

        # Keep inside
        pika_x = max(
            bar_x - pikachu.get_width() // 2,
            min(pika_x, bar_x + bar_w - pikachu.get_width() // 2)
        )

        screen.blit(pikachu, (pika_x, pika_y))
    else:
        # Draw fallback
        pygame.draw.circle(
            screen,
            (255, 204, 0),
            (bar_x + fill_w, bar_y + bar_h // 2),
            18
        )

    # Update screen
    pygame.display.flip()