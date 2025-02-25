import pygame

import constants
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, constants.SHOT_RADIUS)

    def draw(self, screen: pygame.SurfaceType):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
