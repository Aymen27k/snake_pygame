import pygame
import random
import math
from sprite import SpriteManager

class Food:
    def __init__(self, screen_width, screen_height, snake_segments, block_size=20):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.value = 0
        self.time = 0
        self.sparkle_timer = 0
        self.sparkle_active = False
        self.sparkle_pos = None
        self.sparkle_life = 0

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
            self.time += 1

            # Bounce effect
            scale_factor = 1 + 0.15 * math.sin(self.time * 0.30)
            new_size = (
                int(self.block_size * scale_factor),
                int(self.block_size * scale_factor)
            )
            scaled_sprite = pygame.transform.scale(self.current_sprite, new_size)

            offset_x = self.rect.x + (self.block_size - new_size[0]) // 2
            offset_y = self.rect.y + (self.block_size - new_size[1]) // 2

            # --- Sparkle logic ---
            self.sparkle_timer += 1
            if self.sparkle_timer > random.randint(20, 40):
                self.sparkle_timer = 0
                self.sparkle_life = 6
                self.sparkle_active = True
                # random sparkle position near food
                self.sparkle_pos = (
                    offset_x + random.randint(0, new_size[0]),
                    offset_y + random.randint(0, new_size[1])
                )

            if self.sparkle_active and self.sparkle_life > 0 and self.sparkle_pos:
                x, y = self.sparkle_pos
                length = 4
                pygame.draw.line(screen, (255, 255, 255), (x - length, y), (x + length, y))
                pygame.draw.line(screen, (255, 255, 255), (x, y - length), (x, y + length))
                self.sparkle_life -= 1
                if self.sparkle_life == 0:
                    self.sparkle_active = False

            # Draw food
            screen.blit(scaled_sprite, (offset_x, offset_y))
