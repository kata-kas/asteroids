import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

        try:
            self.sounds['dead'] = pygame.mixer.Sound("sounds/dead_sound.wav")
            self.sounds['game_over'] = pygame.mixer.Sound("sounds/game_over.mp3")
            self.sounds['laser'] = pygame.mixer.Sound("sounds/fire.mp3")
            print("Loaded sounds successfully")

        except Exception as e:
            print(f"Error loading sounds: {e}")

    def play(self, sound_name):
        """Play a sound by its name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found")