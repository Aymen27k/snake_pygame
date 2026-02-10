import pygame
from typing import Optional
from sprite import SpriteManager

class Walls:
    def __init__(self, screen_width, screen_height, hud_height, block_size=20):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hud_height = hud_height
        sprites = SpriteManager("assets/snake2.png", block_size=self.block_size)
        # Brick walls
        self.horizontal_wall = sprites.get_sprite(col=12, row=0)
        self.vertical_wall = sprites.get_sprite(col=8, row=2)

        self.walls = []

        # Top row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, self.hud_height, self.block_size, self.block_size)
            self.walls.append((self.horizontal_wall, rect))

        # Bottom row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, self.screen_height - self.block_size, self.block_size, self.block_size)
            self.walls.append((self.horizontal_wall, rect))
        # Left column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(0, y, self.block_size, self.block_size)
            self.walls.append((self.vertical_wall, pygame.Rect(0, y, self.block_size, self.block_size)))

        # Right column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(self.screen_width - self.block_size, y, self.block_size, self.block_size)
            self.walls.append((self.vertical_wall, pygame.Rect(self.screen_width - self.block_size, y, self.block_size, self.block_size)))


        # Grass sprites
        self.horizontal_grass = sprites.get_sprite(col=9, row=1)
        self.vertical_grass = sprites.get_sprite(col=10, row=1)
        self.grass = []
        # Top row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, self.hud_height, self.block_size, self.block_size)
            self.grass.append((self.horizontal_grass, rect))

        # Bottom row
        for x in range(0, self.screen_width, self.block_size):
            rect = pygame.Rect(x, self.screen_height - self.block_size, self.block_size, self.block_size)
            self.grass.append((self.horizontal_grass, rect))
        # Left column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(0, y, self.block_size, self.block_size)
            self.grass.append((self.vertical_grass, pygame.Rect(0, y, self.block_size, self.block_size)))

        # Right column
        for y in range(0, self.screen_height, self.block_size):
            rect = pygame.Rect(self.screen_width - self.block_size, y, self.block_size, self.block_size)
            self.grass.append((self.vertical_grass, pygame.Rect(self.screen_width - self.block_size, y, self.block_size, self.block_size)))


    def draw(self, screen, mode: Optional[str] = "wrap", y_offset=None):
        is_menu = (y_offset == 0)
        sprites_to_draw = self.walls if mode == "classic" else self.grass

        for sprite, rect in sprites_to_draw:
            draw_y = rect.y

            if is_menu and rect.y == self.hud_height:
                draw_y = 0

            screen.blit(sprite, (rect.x, draw_y))

    def check_collision(self, snake, screen_width, screen_height, mode: Optional[str] = "wrap", override_hud=None):
        current_hud = override_hud if override_hud is not None else self.hud_height
        effective_top = current_hud + self.block_size
        if mode == "wrap":
            # Teleport logic
            if snake.head.top < effective_top:
                snake.head.bottom = screen_height - self.block_size
            elif snake.head.bottom > screen_height - self.block_size:
                snake.head.top = effective_top
            elif snake.head.left < self.block_size:
                snake.head.right = screen_width - self.block_size
            elif snake.head.right > screen_width - self.block_size:
                snake.head.left = self.block_size
        elif mode == "classic":
            if (snake.head.top < effective_top or
                snake.head.bottom > screen_height - self.block_size or
                snake.head.left < self.block_size or
                snake.head.right > screen_width - self.block_size):
                return True
        return False
