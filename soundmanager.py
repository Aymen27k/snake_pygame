import pygame
from path_util import resource_path

class SoundManager:
    def __init__(self, is_enabled):
        pygame.mixer.init()
        self.enabled = is_enabled
        self.sounds = {
        "eat": pygame.mixer.Sound(resource_path("assets/sfx/eat.mp3")),
        "game_over": pygame.mixer.Sound(resource_path("assets/sfx/game_over.mp3")),
        "speed_up": pygame.mixer.Sound(resource_path("assets/sfx/speed_up.mp3")),
        "dmg": pygame.mixer.Sound(resource_path("assets/sfx/dmg.mp3")),
        "explosion": pygame.mixer.Sound(resource_path("assets/sfx/explosion.mp3")),
        "scream": pygame.mixer.Sound(resource_path("assets/sfx/scream.mp3")),
        "boss_dmg": pygame.mixer.Sound(resource_path("assets/sfx/boss_dmg.mp3")),
        "poison_get": pygame.mixer.Sound(resource_path("assets/sfx/poison_get.mp3")),
        "shoot": pygame.mixer.Sound(resource_path("assets/sfx/shoot.mp3")),
        "browse_menu": pygame.mixer.Sound(resource_path("assets/sfx/browse_menu.mp3")),
        "menu_selection": pygame.mixer.Sound(resource_path("assets/sfx/menu_selection.mp3")),
        "sfx_off": pygame.mixer.Sound(resource_path("assets/sfx/sfx_off.mp3")),
        }
    def toggle(self):
        self.enabled = not self.enabled
        if not self.enabled:
            return self.enabled

    def play(self, name):
        if not self.enabled:
            return
        if name in self.sounds:
            self.sounds[name].play()

    def stop(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
