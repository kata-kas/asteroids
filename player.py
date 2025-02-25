from circleshape import CircleShape
import constants
import pygame

from shot import Shot


class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a,b,c]

    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt: int):
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt: int):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation += constants.PLAYER_TURN_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation -= constants.PLAYER_TURN_SPEED * dt
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.timer -= dt
            if self.timer <= 0:
                return self.shoot()

    def move(self, dt: int):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_SPEED * dt

    def shoot(self):
        self.timer = constants.PLAYER_SHOOT_COOLDOWN
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = forward * constants.PLAYER_SHOT_SPEED
        return shot