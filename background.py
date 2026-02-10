import pygame
from path_util import resource_path

class Background:
    def __init__(self, screen, screen_width, screen_height, hud_height, bg_path=resource_path("assets/grass_bg.png"), block_size=20):
        self.screen = screen
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hud_height = hud_height
        self.playable_height = screen_height - hud_height
        #self.grass_tile = sprites.get_sprite(col=..., row=...)  # your grassy tile
        #self.stone_tile = sprites.get_sprite(col=..., row=...)  # your cracked stone tile
        #self.stone_positions = self.generate_stone_positions()
        # 1. The Game Version (Short)
        raw_image = pygame.image.load(bg_path).convert()
        self.game_bg = pygame.transform.scale(raw_image, (screen_width, screen_height - hud_height))

        # 2. The Menu Version (Full Height) [cite: 2024-12-19]
        self.menu_bg = pygame.transform.scale(raw_image, (screen_width, screen_height))


    def draw(self, is_menu=False):
        if is_menu:
            # Draw the full-height version at the very top [cite: 2024-12-19]
            self.screen.blit(self.menu_bg, (0, 0))
        else:
            # Draw the short version below the HUD [cite: 2024-12-19]
            self.screen.blit(self.game_bg, (0, self.hud_height))
