import pygame
import random

class Alien:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.block_size = block_size
        self.move_speed = 5  # Moves 2 pixels per frame
        self.is_moving = False
        self.boss_size = block_size * 4
        self.image = pygame.image.load("assets/alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.boss_size, self.boss_size))
        self.image.set_colorkey((0, 0, 0))

        self.health = 5
        # 2. Position (Grid-aligned)
        self.x = random.randrange(0, screen_width - self.boss_size, block_size)
        self.y = random.randrange(0, screen_height - self.boss_size, block_size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.target_x = self.x
        self.target_y = self.y

    def draw(self, screen):
        # Draw the sprite instead of a colored box
        screen.blit(self.image, self.rect)

    def update(self):
        # 1. SLIDE: Move 2 pixels toward the target every frame
        if self.rect.x < self.target_x:
            self.rect.x += self.move_speed
        elif self.rect.x > self.target_x:
            self.rect.x -= self.move_speed

        if self.rect.y < self.target_y:
            self.rect.y += self.move_speed
        elif self.rect.y > self.target_y:
            self.rect.y -= self.move_speed

        # 2. ARRIVED: If we are exactly at the target, pick the next grid square
        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            
            # Pick a random direction: Left, Right, Up, or Down
            dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            
            # Calculate where that next 20px step would be
            possible_x = self.rect.x + (dx * self.block_size)
            possible_y = self.rect.y + (dy * self.block_size)

            # 3. BOUNDARY CHECK: Only update target if it's inside the screen
            if 0 <= possible_x <= self.screen_width - self.boss_size:
                self.target_x = possible_x
                
            if 0 <= possible_y <= self.screen_height - self.boss_size:
                self.target_y = possible_y