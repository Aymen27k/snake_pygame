import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "eat": pygame.mixer.Sound("assets/sfx/eat.mp3"),
            "game_over": pygame.mixer.Sound("assets/sfx/game_over.mp3"),
            "speed_up": pygame.mixer.Sound("assets/sfx/speed_up.mp3"),
        }

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def stop(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
