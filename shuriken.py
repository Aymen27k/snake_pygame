import pygame

class Shuriken:
    def __init__(self, x, y, dx, dy, ammo_sprite):
        self.image = ammo_sprite
        self.rect = self.image.get_rect(center=(x, y))

        self.dx = dx
        self.dy = dy
        self.speed = 5

    def update(self):
        # Now self.rect.x will work!
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)