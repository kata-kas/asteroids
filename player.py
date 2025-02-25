from circleshape import CircleShape
import constants
import pygame

from shot import Shot


class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.sprite = pygame.image.load("sprites/spaceship.png").convert_alpha()
        # Adjust sprite size to match player radius
        self.sprite = pygame.transform.scale(self.sprite,
                                             (self.radius * 2, self.radius * 2))
        self.original_sprite = self.sprite.copy()  # Keep an original copy for rotation

        # Lives system
        self.lives = constants.PLAYER_INITIAL_LIVES
        self.invulnerable_timer = 0
        self.is_invulnerable = False
        self.blink_timer = 0
        self.visible = True
        self.initial_position = pygame.Vector2(x, y)

    def draw(self, screen: pygame.SurfaceType):
        # Don't draw if blinking and not visible
        if self.is_invulnerable and not self.visible:
            return

        # Rotate the sprite
        rotated_sprite = pygame.transform.rotate(self.original_sprite, -self.rotation)
        # Get the rect for positioning
        sprite_rect = rotated_sprite.get_rect(center=self.position)
        # Draw the sprite
        screen.blit(rotated_sprite, sprite_rect)

        # Optional: draw collision circle for debugging
        # pygame.draw.circle(screen, "red", self.position, self.radius, 1)

    def update(self, dt: int):
        # Update invulnerability
        if self.is_invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False
                self.visible = True

            # Blink effect while invulnerable
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.blink_timer = constants.PLAYER_BLINK_RATE
                self.visible = not self.visible

        # Process input only if alive
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
        # Invert the forward vector to match sprite orientation
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_SPEED * dt

        # Wrap around screen edges
        if self.position.x < 0:
            self.position.x = constants.SCREEN_WIDTH
        if self.position.x > constants.SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = constants.SCREEN_HEIGHT
        elif self.position.y > constants.SCREEN_HEIGHT:
            self.position.y = 0

    def shoot(self):
        self.timer = constants.PLAYER_SHOOT_COOLDOWN
        # Invert the forward vector to match sprite orientation
        forward = pygame.Vector2(0, -1).rotate(self.rotation)

        # Calculate the position at the front of the ship
        shot_pos = self.position + forward * self.radius
        shot = Shot(shot_pos.x, shot_pos.y)
        shot.velocity = forward * constants.PLAYER_SHOT_SPEED
        return shot

    def lose_life(self):
        # Only lose a life if not invulnerable
        if not self.is_invulnerable:
            self.lives -= 1
            return True
        return False

    def respawn(self):
        # Reset position to center
        self.position = self.initial_position.copy()
        # Reset velocity
        self.velocity = pygame.Vector2(0, 0)
        # Make invulnerable
        self.is_invulnerable = True
        self.invulnerable_timer = constants.PLAYER_INVULNERABLE_TIME
        self.blink_timer = constants.PLAYER_BLINK_RATE
        self.visible = True

    def is_alive(self):
        return self.lives > 0