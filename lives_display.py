import pygame

class LivesDisplay:
    def __init__(self):
        # Load the ship sprite for lives display
        self.life_sprite = pygame.image.load("sprites/spaceship.png").convert_alpha()
        # Scale it down for the UI
        self.life_sprite = pygame.transform.scale(self.life_sprite, (20, 20))
        # Rotate it to point upward
        self.life_sprite = pygame.transform.rotate(self.life_sprite, 0)

    def draw(self, screen: pygame.SurfaceType, lives: int):
        # Draw lives in the top-left corner
        for i in range(lives):
            x = 20 + i * 30  # Position each life icon with some spacing
            y = 20  # Fixed y position
            screen.blit(self.life_sprite, (x, y))

        # Optional: Draw text "LIVES: X" instead of or in addition to icons
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"LIVES: {lives}", True, (255, 255, 255))
        screen.blit(text, (20, 50))