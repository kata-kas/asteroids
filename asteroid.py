import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x: int, y: int, radius: int):
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.SurfaceType):
        pygame.draw.circle(screen, "white", self.position, self.radius, 0)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)
        vec1 = self.velocity.rotate(random_angle)
        vec2 = self.velocity.rotate(-random_angle)
        asteroid1 = Asteroid(self.position.x, self.position.y, self.radius // 2)
        asteroid1.velocity = vec1
        asteroid2 = Asteroid(self.position.x, self.position.y, self.radius // 2)
        asteroid2.velocity = vec2