import random
import pygame
from sprite import SpriteManager


class Snake:
    def __init__(self, screen_width, screen_height, block_size=20) -> None:
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.segments: list[pygame.Rect] = []
        self.direction = "RIGHT"
        self.max_snake_length = float("inf")
        self.create_snake()
        self.head = self.segments[0]
        self.tail = self.segments[-1]
        self.is_paused = False
        self.should_grow = False
        sprites = SpriteManager("assets/snake2.png", block_size=self.block_size)
        self.head_right = sprites.get_sprite(col=4, row=3)
        self.head_left = sprites.get_sprite(col=2, row=3)
        self.head_up = sprites.get_sprite(col=1, row=3)
        self.head_down = sprites.get_sprite(col=3, row=3)
        self.body_sprite = sprites.get_sprite(5, 3)



    
    def create_snake(self):
        start_x, start_y = 400, 300
        self.segments = [
        pygame.Rect(start_x, start_y, self.block_size, self.block_size),
        pygame.Rect(start_x - self.block_size, start_y, self.block_size, self.block_size),
        pygame.Rect(start_x - 2*self.block_size, start_y, self.block_size, self.block_size)
        ]


    def move(self, direction, growth=False):
            head_x = self.segments[0].x
            head_y = self.segments[0].y

            # 1. Calculate new coordinates
            if direction == "UP":
                head_y -= self.block_size
            elif direction == "DOWN":
                head_y += self.block_size
            elif direction == "LEFT":
                head_x -= self.block_size
            elif direction == "RIGHT":
                head_x += self.block_size

            # 2. Insert new head
            new_head = pygame.Rect(head_x, head_y, self.block_size, self.block_size)
            self.segments.insert(0, new_head)

            # --- THE FIX IS HERE ---
            # Check the flag before we decide to remove the tail
            if self.should_grow:
                growth = True
                self.should_grow = False 
            # -----------------------

            # 3. Remove tail (unless growing)
            if not growth:
                self.segments.pop()

            # 4. Update head/tail references
            self.head = self.segments[0]
            self.tail = self.segments[-1]

    def draw(self, screen, direction):
        if direction == "RIGHT":
            head_sprite = self.head_right
        elif direction == "LEFT":
            head_sprite = self.head_left
        elif direction == "UP":
            head_sprite = self.head_up
        elif direction == "DOWN":
            head_sprite = self.head_down
        else:
            head_sprite = self.head_right

        screen.blit(head_sprite, (self.segments[0].x, self.segments[0].y))

        for segment in self.segments[1:]:
            screen.blit(self.body_sprite, (segment.x, segment.y))


    def check_self_collision(self):
        for segment in self.segments[1:]:
            if self.head.colliderect(segment):
                return True
        return False

    def move_auto(self, screen):
        # Occasionally change direction
        if random.randint(0, 100) < 10:  # 10% chance per frame
            new_direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            if not self.is_opposite_direction(new_direction):
                self.direction = new_direction
        # Menu snake random Growth
        if len(self.segments) < self.max_snake_length:
            random_growth = random.randint(0, 100) < 2
        else:
            random_growth = False

        # Move in current direction
        self.move(self.direction, growth=random_growth)
        self.draw(screen, self.direction)
    def is_opposite_direction(self, new_direction):
        opposites = {
            "UP" : "DOWN",
            "DOWN" : "UP",
            "LEFT" : "RIGHT",
            "RIGHT" : "LEFT"
        }
        return opposites[self.direction] == new_direction
