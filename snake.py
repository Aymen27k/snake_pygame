import random
import pygame
from sprite import SpriteManager


class Snake:
    def __init__(self, screen_width, screen_height, hud_height, block_size=20) -> None:
        self.block_size = block_size
        self.screen_width = screen_width
        self.hud_height = hud_height
        self.screen_height = screen_height
        self.segments: list[pygame.Rect] = []
        self.direction = "RIGHT"
        self.max_snake_length = float("inf")
        self.poison_ammo = 0
        self.create_snake()
        self.head = self.segments[0]
        self.tail = self.segments[-1]
        self.is_paused = False
        self.should_grow = False
        self.is_dead = False
        self.last_damage_time = -1000
        self.damage_cooldown = 500
        sprites = SpriteManager("assets/snake2.png", block_size=self.block_size)
        self.head_right = sprites.get_sprite(col=4, row=3)
        self.head_left = sprites.get_sprite(col=2, row=3)
        self.head_up = sprites.get_sprite(col=1, row=3)
        self.head_down = sprites.get_sprite(col=3, row=3)
        self.body_sprite = sprites.get_sprite(5, 3)



    def create_snake(self):
        start_x = (self.screen_width // 2)
        start_y = self.hud_height + ((self.screen_height - self.hud_height) // 2 // self.block_size) * self.block_size
        self.segments = [
        pygame.Rect(start_x, start_y, self.block_size, self.block_size),
        pygame.Rect(start_x - self.block_size, start_y, self.block_size, self.block_size),
        pygame.Rect(start_x - 2*self.block_size, start_y, self.block_size, self.block_size)
        ]

    def reset(self):
        self.create_snake() # Re-centers the snake and resets segments
        self.head = self.segments[0]
        self.tail = self.segments[-1]
        self.direction = "RIGHT"
        self.is_dead = False
        self.should_grow = False
        self.poison_ammo = 0
        self.last_damage_time = -1000 # Clear the hurt timer
        # Any other status effects like poison_ammo should also reset here
        
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

        if self.should_grow:
            growth = True
            self.should_grow = False


        # 3. Remove tail (unless growing)
        if not growth:
            self.segments.pop()

        # 4. Update head/tail references
        self.head = self.segments[0]
        self.tail = self.segments[-1]

    def draw(self, screen, direction):
        current_time = pygame.time.get_ticks()

        # Pick correct head sprite
        if direction == "RIGHT":
            head_sprite = self.head_right.copy()
        elif direction == "LEFT":
            head_sprite = self.head_left.copy()
        elif direction == "UP":
            head_sprite = self.head_up.copy()
        elif direction == "DOWN":
            head_sprite = self.head_down.copy()
        else:
            head_sprite = self.head_right.copy()

        # Copy body sprite for safe modifications
        body_sprite = self.body_sprite.copy()

        # Check cooldown for invincibility
        time_since_damage = current_time - self.last_damage_time
        if time_since_damage < self.damage_cooldown:
            # Rapid flicker: Only draw if the 50ms pulse is even
            if (current_time // 50) % 2 == 0:
                return

            head_sprite.set_alpha(150)
            body_sprite.set_alpha(150)

        # Draw head
        screen.blit(head_sprite, (self.head.x, self.head.y))

        # Draw body
        for segment in self.segments[1:]:
            screen.blit(body_sprite, (segment.x, segment.y))

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

    def take_damage(self, current_time, amount=1):
        if current_time - self.last_damage_time > self.damage_cooldown and not self.is_dead:
            # 1. Apply the damage first
            for _ in range(amount):
                if len(self.segments) > 1:
                    self.segments.pop()
            
            # 2. Update the timestamp so invincibility starts
            self.last_damage_time = current_time

            # 3. Check for death AFTER all segments are removed
            # If only the head remains and we try to take more damage, or length is too low:
            if len(self.segments) < 2: 
                self.is_dead = True
                return "KILLED"

            return "HIT"
        return "COOLDOWN"

    def can_attack(self, current_time):
        return (current_time - self.last_damage_time) >= self.damage_cooldown and not self.is_dead
