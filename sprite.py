import pygame


class SpriteManager:
    def __init__(self, sheet_path, block_size=20, tile_size=8):
        self.sheet = pygame.image.load(sheet_path).convert_alpha()
        self.block_size = block_size
        self.tile_size = tile_size

    def get_sprite(self, col, row):
        x = col * self.tile_size
        y = row * self.tile_size
        sprite = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, self.tile_size, self.tile_size))
        # Scale once here
        return pygame.transform.scale(sprite, (self.block_size, self.block_size))
