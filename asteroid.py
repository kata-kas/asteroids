import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT


class Asteroid(CircleShape):
    def __init__(self, x: int, y: int, radius: int):
        super().__init__(x, y, radius)
        asteroid_type = random.choice(["asteroid1", "asteroid2"])
        self.sprite = pygame.image.load(f"sprites/{asteroid_type}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (radius * 2, radius * 2))
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-20, 20)

    def draw(self, screen: pygame.SurfaceType):
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        sprite_rect = rotated_sprite.get_rect(center=self.position)
        screen.blit(rotated_sprite, sprite_rect)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt

        # Wrap around screen edges
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

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