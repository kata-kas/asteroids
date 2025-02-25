import pygame
import math

import constants
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, constants.SHOT_RADIUS)
        self.sprite = pygame.image.load("sprites/laser.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (
        constants.SHOT_RADIUS * 2, constants.SHOT_RADIUS * 4))
        self.original_sprite = self.sprite.copy()
        self.rotation = 0

    def draw(self, screen: pygame.SurfaceType):
        if self.velocity.length() > 0:
            self.rotation = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
        rotated_sprite = pygame.transform.rotate(self.original_sprite, self.rotation)
        sprite_rect = rotated_sprite.get_rect(center=self.position)
        screen.blit(rotated_sprite, sprite_rect)

    def update(self, dt):
        self.position += self.velocity * dt

        if not (0 <= self.position.x <= constants.SCREEN_WIDTH and 0 <= self.position.y <= constants.SCREEN_HEIGHT):
            self.kill()