import pygame
from typing import Optional
from sprite import SpriteManager

class Walls:
    def __init__(self, screen_width, screen_height, block_size=20):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        sprites = SpriteManager("assets/snake2.png", block_size=self.block_size)
        # Brick walls
        self.horizontal_wall = sprites.get_sprite(col=12, row=0)
        self.vertical_wall = sprites.get_sprite(col=8, row=2)

        self.walls = []

        # Top row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, 0, self.block_size, self.block_size)
            self.walls.append((self.horizontal_wall, rect))

        # Bottom row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, self.screen_height - self.block_size, self.block_size, self.block_size)
            self.walls.append((self.horizontal_wall, rect))
        # Left column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(0, y, self.block_size, self.block_size)
            self.walls.append((self.vertical_wall, rect))

        # Right column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(self.screen_width - self.block_size, y, self.block_size, self.block_size)
            self.walls.append((self.vertical_wall, rect))


        # Grass sprites
        self.horizontal_grass = sprites.get_sprite(col=9, row=1)
        self.vertical_grass = sprites.get_sprite(col=10, row=1)
        self.grass = []
        # Top row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, 0, self.block_size, self.block_size)
            self.grass.append((self.horizontal_grass, rect))

        # Bottom row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, self.screen_height - self.block_size, self.block_size, self.block_size)
            self.grass.append((self.horizontal_grass, rect))
        # Left column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(0, y, self.block_size, self.block_size)
            self.grass.append((self.vertical_grass, rect))

        # Right column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(self.screen_width - self.block_size, y, self.block_size, self.block_size)
            self.grass.append((self.vertical_grass, rect))



    def draw(self, screen, mode: Optional[str] = "wrap"):
        if mode == "classic":
            for sprite, rect in self.walls:
                screen.blit(sprite, (rect.x, rect.y))
        else:
            for sprite, rect in self.grass:
                screen.blit(sprite, (rect.x, rect.y))

    def check_collision(self, snake, screen_width, screen_height, mode: Optional[str] = "wrap"):
        if mode == "wrap":
            # Teleport logic
            if snake.head.top < self.block_size:
                snake.head.bottom = screen_height - self.block_size
            elif snake.head.bottom > screen_height - self.block_size:
                snake.head.top = self.block_size
            elif snake.head.left < self.block_size:
                snake.head.right = screen_width - self.block_size
            elif snake.head.right > screen_width - self.block_size:
                snake.head.left = self.block_size
        elif mode == "classic":
            # Deadly walls logic
            if (snake.head.top < self.block_size or
                snake.head.bottom > screen_height - self.block_size or
                snake.head.left < self.block_size or
                snake.head.right > screen_width - self.block_size):
                return True  # collision detected
        return False
