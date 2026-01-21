import pygame
import random
from sprite import SpriteManager

class Food:
    def __init__(self, screen_width, screen_height, snake_segments, block_size=20):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.value = 0
        sprites = SpriteManager("assets/snake2.png", block_size=self.block_size)
        self.normal_foods = [
            sprites.get_sprite(6, 0),  # red apple
            sprites.get_sprite(6, 1),  # yellow apple
            sprites.get_sprite(6, 4)   # green apple
        ]

        self.special_foods = [
            sprites.get_sprite(6, 3),  # cherry
            sprites.get_sprite(7, 3)   # cookie
        ]


        # Create initial food rect
        self.rect = pygame.Rect(0, 0, block_size, block_size)
        self.color = (0, 0, 255)  # blue
        self.refresh(snake_segments)

    def refresh(self, snake_segments):
        while True:
            # Keep food inside the playable area (avoid walls)
            grid_min_x = 1
            grid_max_x = (self.screen_width // self.block_size) - 2
            grid_min_y = 1
            grid_max_y = (self.screen_height // self.block_size) - 2

            random_x = random.randint(grid_min_x, grid_max_x) * self.block_size
            random_y = random.randint(grid_min_y, grid_max_y) * self.block_size


            new_rect = pygame.Rect(random_x, random_y, self.block_size, self.block_size)

            # Check against snake body
            if not any(segment.colliderect(new_rect) for segment in snake_segments):
                self.rect = new_rect
                # Special food spawning rate
                if random.random() < 0.1:
                    self.current_sprite = random.choice(self.special_foods)
                    self.value = 5
                else:
                    self.current_sprite = random.choice(self.normal_foods)
                    self.value = 1
                break


    def draw(self, screen, snake):
        if not snake.is_paused:
            screen.blit(self.current_sprite, (self.rect.x, self.rect.y))
