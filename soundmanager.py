import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "eat": pygame.mixer.Sound("assets/sfx/eat.mp3"),
            "game_over": pygame.mixer.Sound("assets/sfx/game_over.mp3"),
            "speed_up": pygame.mixer.Sound("assets/sfx/speed_up.mp3"),
            "dmg": pygame.mixer.Sound("assets/sfx/dmg.mp3"),
            "explosion": pygame.mixer.Sound("assets/sfx/explosion.mp3"),
            "scream": pygame.mixer.Sound("assets/sfx/scream.mp3"),
            "boss_dmg": pygame.mixer.Sound("assets/sfx/boss_dmg.mp3"),
        }

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def stop(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
