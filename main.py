import pygame
import constants
from animated_background import AnimatedBackground
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot
from lives_display import LivesDisplay
from sound_manager import SoundManager


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    sound_manager = SoundManager()

    try:
        background = AnimatedBackground("sprites/bg.gif", brightness=0.3)
    except Exception as e:
        print(f"Error loading background: {e}")
        background = None

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = updatable, drawable
    Asteroid.containers = updatable, drawable, asteroids
    AsteroidField.containers = updatable
    Shot.containers = updatable, drawable, shots

    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, sound_manager)
    lives_display = LivesDisplay()
    AsteroidField()

    game_over = False
    respawn_timer = 0
    respawning = False
    game_over_sound_played = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if background:
            background.update(dt)
            background.draw(screen)
        else:
            screen.fill("black")

        if game_over:
            if not game_over_sound_played:
                sound_manager.play('game_over')
                game_over_sound_played = True

            font = pygame.font.SysFont(None, 72)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2))
            screen.blit(game_over_text, text_rect)

            font = pygame.font.SysFont(None, 36)
            restart_text = font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 50))
            screen.blit(restart_text, restart_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                player.kill()
                for asteroid in asteroids:
                    asteroid.kill()
                for shot in shots:
                    shot.kill()

                player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
                AsteroidField()
                game_over = False
                game_over_sound_played = False

            pygame.display.flip()
            dt = clock.tick(60) / 1000
            continue

        if respawning:
            respawn_timer -= dt
            if respawn_timer <= 0:
                respawning = False
                player.respawn()

        for obj in drawable:
            obj.draw(screen)
        for obj in updatable:
            obj.update(dt)

        if player.alive() and not respawning:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if player.lose_life():
                        sound_manager.play('dead')

                        if player.is_alive():
                            respawning = True
                            respawn_timer = constants.PLAYER_RESPAWN_DELAY
                        else:
                            game_over = True
                    break

        for asteroid in list(asteroids):
            for shot in list(shots):
                if asteroid.collides_with(shot):
                    new_asteroids = asteroid.split()
                    if new_asteroids:
                        asteroids.add(new_asteroids)
                    shot.kill()
                    break

        lives_display.draw(screen, player.lives)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()