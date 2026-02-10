import pygame

class MusicManager:
    def __init__(self, is_enabled):
        pygame.mixer.init()
        self.current_state = None
        self.enabled = is_enabled
        self.tracks = {
            "menu": "assets/music/main_menu_music.mp3",
            "gameplay": "assets/music/gameplay_music.mp3",
            "ultra": "assets/music/ultra_speed_music.mp3",
            "game_over": "assets/music/game_over.mp3"
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
