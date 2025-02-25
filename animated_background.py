import pygame
from PIL import Image, ImageSequence, ImageEnhance
import constants


class AnimatedBackground:
    def __init__(self, path, brightness=0.5):
        """
        Initialize animated background with brightness control

        Args:
            path: Path to the GIF file
            brightness: Float between 0.0 (completely dark) and 1.0 (original brightness)
        """
        self.frames = []
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = 0.1  # Default frame duration (100ms)
        self.brightness = max(0.0, min(1.0, brightness))  # Clamp between 0 and 1

        # Load the GIF using PIL
        try:
            gif = Image.open(path)

            # Get frame durations (convert to seconds)
            durations = []
            for frame in ImageSequence.Iterator(gif):
                duration = frame.info.get('duration', 100)  # Default 100ms if not specified
                durations.append(duration / 1000.0)  # Convert ms to seconds

            # Calculate average frame duration if there are multiple frames
            if durations:
                self.frame_duration = sum(durations) / len(durations)

            # Convert each frame to a PyGame surface with brightness adjustment
            for frame in ImageSequence.Iterator(gif):
                # Convert PIL Image to RGBA
                frame_rgba = frame.convert('RGBA')

                # Apply brightness adjustment
                if self.brightness < 1.0:
                    # Create a brightness enhancer and adjust
                    enhancer = ImageEnhance.Brightness(frame_rgba)
                    frame_rgba = enhancer.enhance(self.brightness)

                # Convert to PyGame surface
                frame_data = frame_rgba.tobytes()
                frame_size = frame_rgba.size
                pygame_frame = pygame.image.fromstring(frame_data, frame_size, 'RGBA')

                # Scale if needed
                if frame_size[0] != constants.SCREEN_WIDTH or frame_size[1] != constants.SCREEN_HEIGHT:
                    pygame_frame = pygame.transform.scale(pygame_frame,
                                                          (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

                self.frames.append(pygame_frame)

            print(f"Loaded {len(self.frames)} frames from GIF")

        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Create a fallback frame (dark background with stars)
            fallback = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            fallback.fill((0, 0, 0))
            # Add some stars
            for _ in range(50):
                x = pygame.randint(0, constants.SCREEN_WIDTH - 1)
                y = pygame.randint(0, constants.SCREEN_HEIGHT - 1)
                fallback.set_at((x, y), (255, 255, 255))
            self.frames = [fallback]

    def apply_overlay(self, surface, alpha=128):
        """Apply a dark overlay to further dim the background"""
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        surface.blit(overlay, (0, 0))

    def update(self, dt):
        # Only update if we have multiple frames
        if len(self.frames) > 1:
            self.animation_time += dt
            if self.animation_time >= self.frame_duration:
                self.animation_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        if self.frames:
            # Create a copy of the current frame to avoid modifying the original
            current_frame = self.frames[self.current_frame].copy()

            # Apply a dark overlay for additional dimming if needed
            if self.brightness > 0.3:  # Only apply overlay if not already very dark
                self.apply_overlay(current_frame, int(128 * (1 - self.brightness)))

            screen.blit(current_frame, (0, 0))