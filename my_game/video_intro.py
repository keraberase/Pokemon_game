import pygame
from config import *

# Try OpenCV
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False


class VideoIntro:

    def __init__(self, path):
        # Default state
        self.available = False
        self.cap = None
        self.finished = False
        self.current_surface = None
        self.frame_delay_ms = 1000 / 30
        self.next_frame_time = 0
        self.stop_frames_before_end = 4

        # Check OpenCV
        if not CV2_AVAILABLE:
            return

        # Load video
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            cap.release()
            return

        # Save video
        self.cap = cap

        # Get FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        self.frame_delay_ms = 1000.0 / fps if fps and fps > 1 else 1000.0 / 30

        # Start video
        self.available = True
        self.next_frame_time = pygame.time.get_ticks()
        self._advance_frame()

    def _advance_frame(self):
        # Stop if done
        if self.finished or self.cap is None:
            return

        # Read frame
        ok, frame = self.cap.read()
        if not ok:
            self.finished = True
            self.cap.release()
            self.cap = None
            return

        # Check position
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # Stop early
        if total_frames > 0 and current_frame >= total_frames - self.stop_frames_before_end:
            self.finished = True
            self.cap.release()
            self.cap = None
            return

        # Convert colors
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Make surface
        h, w = frame.shape[:2]
        surface = pygame.image.frombuffer(frame.tobytes(), (w, h), "RGB")

        # Fit screen
        self.current_surface = self._fit_to_screen(surface)

    @staticmethod
    def _fit_to_screen(surface):
        # Get size
        w, h = surface.get_size()

        # Fill screen
        scale = max(SCREEN_W / w, SCREEN_H / h)
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        scaled = pygame.transform.smoothscale(surface, new_size)

        # Crop center
        x = (scaled.get_width() - SCREEN_W) // 2
        y = (scaled.get_height() - SCREEN_H) // 2
        return scaled.subsurface((x, y, SCREEN_W, SCREEN_H)).copy()

    def update(self):
        # Skip update
        if not self.available or self.finished:
            return

        # Frame timing
        now = pygame.time.get_ticks()
        if now >= self.next_frame_time:
            self._advance_frame()
            self.next_frame_time = now + self.frame_delay_ms

    def draw(self, screen):
        # Clear screen
        screen.fill((0, 0, 0))

        # Draw frame
        if self.current_surface is not None:
            x = (SCREEN_W - self.current_surface.get_width()) // 2
            y = (SCREEN_H - self.current_surface.get_height()) // 2
            screen.blit(self.current_surface, (x, y))