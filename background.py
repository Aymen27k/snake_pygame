import pygame

class Background:
    def __init__(self, screen, screen_width, screen_height, bg_path="assets/grass_bg.png", block_size=20):
        self.screen = screen
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        #self.grass_tile = sprites.get_sprite(col=..., row=...)  # your grassy tile
        #self.stone_tile = sprites.get_sprite(col=..., row=...)  # your cracked stone tile
        #self.stone_positions = self.generate_stone_positions()
        self.background_img = pygame.transform.scale(
        pygame.image.load(bg_path).convert(),
        (screen_width, screen_height)
)


    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
