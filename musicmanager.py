import pygame
from path_util import resource_path

class MusicManager:
    def __init__(self, is_enabled):
        pygame.mixer.init()
        self.current_state = None
        self.enabled = is_enabled
        self.tracks = {
        "menu": resource_path("assets/music/main_menu_music.mp3"),
        "gameplay": resource_path("assets/music/gameplay_music.mp3"),
        "ultra": resource_path("assets/music/ultra_speed_music.mp3"),
        "game_over": resource_path("assets/music/game_over.mp3")
        }

    def toggle(self):
        self.enabled = not self.enabled
        if not self.enabled:
            pygame.mixer.music.stop()
            self.current_state = None
        return self.enabled

    def play(self, state, loop=-1, volume=0.5, fade_ms=1000):
        # Only switch if state changes
        if not self.enabled:
            return
        if state != self.current_state:
            pygame.mixer.music.fadeout(fade_ms)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.tracks[state])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop, fade_ms=fade_ms)
            self.current_state = state

    def stop(self):
        pygame.mixer.music.stop()
        self.current_state = None
