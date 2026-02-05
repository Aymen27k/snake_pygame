import pygame

class PoisonProjectile:
    def __init__(self, x, y, direction, block_size=20):
        self.rect = pygame.Rect(x, y, block_size // 2, block_size // 2)
        self.direction = direction
        self.speed = 25 # Faster than the snake!
        self.active = True

    def update(self):
        if self.direction == "UP":    self.rect.y -= self.speed
        if self.direction == "DOWN":  self.rect.y += self.speed
        if self.direction == "LEFT":  self.rect.x -= self.speed
        if self.direction == "RIGHT": self.rect.x += self.speed

        # Deactivate if it goes off screen
        if self.rect.x < 0 or self.rect.x > 800 or self.rect.y < 0 or self.rect.y > 600:
            self.active = False

    def draw(self, screen):
        # A simple toxic green/purple circle for the shot
        pygame.draw.circle(screen, (128, 0, 128), self.rect.center, 6)