import pygame
import random
import shuriken
from sprite import SpriteManager

class Alien:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boss_alive = True
        self.is_spawning = True
        self.intro_triggered = False
        self.spawn_timer = pygame.time.get_ticks()
        self.health = 5
        self.block_size = block_size
        self.move_speed = 5
        self.boss_size = block_size * 4
        self.behavior_counter = 0
        self.hit_cooldown = 500 
        self.last_hit_time = 0
        
        # Graphics
        self.image = pygame.image.load("assets/alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.boss_size, self.boss_size))
        self.image.set_colorkey((0, 0, 0))

        # Projectiles
        sprites = SpriteManager("assets/snake2.png", block_size=self.block_size)
        self.shuriken_image = sprites.get_sprite(col=6, row=6)
        self.shurikens = []
        self.last_shot_time = 0
        self.shoot_cooldown = 2000

        # Position
        self.x = random.randrange(0, screen_width - self.boss_size, block_size)
        self.y = random.randrange(0, screen_height - self.boss_size, block_size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.target_x = self.x
        self.target_y = self.y


        self.reset()

    def reset(self):
        """Call this to restart the boss completely"""
        self.boss_alive = True
        self.is_spawning = True
        self.intro_triggered = False
        self.spawn_timer = 0 # Syncs the flash timer!
        self.health = 5  # Set your starting health

        self.behavior_counter = 0
        self.last_hit_time = -1000
        self.shurikens = []
        self.last_shot_time = 0
        self.shoot_cooldown = 2000
        self.move_speed = 5

        # Randomize position
        self.x = random.randrange(0, self.screen_width - self.boss_size, self.block_size)
        self.y = random.randrange(0, self.screen_height - self.boss_size, self.block_size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.target_x = self.x
        self.target_y = self.y

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        
        # 1. Start with a fresh copy of the image
        temp_image = self.image.copy()
        
        # Calculate how long it has been since the last hit
        time_since_hit = current_time - self.last_hit_time

        # --- 2. THE "HURT" STATE (Flashing & Transparency) ---
        if time_since_hit < self.hit_cooldown:
            # Ghost effect: Make him semi-transparent (120 is about 47% opacity)
            temp_image.set_alpha(120)
            
            # Strobe effect: Toggle Red/White every 100ms
            if (current_time // 100) % 2 == 0:
                temp_image.fill((255, 255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                temp_image.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

        # --- 3. THE "SPAWNING" STATE (Only if NOT currently hurt) ---
        elif self.is_spawning:
            temp_image.set_alpha(150)
            
        # --- 4. THE "NORMAL" STATE ---
        else:
            temp_image.set_alpha(255)

        # 5. Final render to screen
        screen.blit(temp_image, self.rect)

    def update(self, player_x, player_y):
        current_time = pygame.time.get_ticks()

        # 1. Spawning Pause (Keeps him still for 1.5s)
        if self.is_spawning:
            if current_time - self.spawn_timer > 1500:
                self.is_spawning = False
            return

        # --- 1. THE LEGS: Just sliding ---
        if self.rect.x < self.target_x: self.rect.x += self.move_speed
        elif self.rect.x > self.target_x: self.rect.x -= self.move_speed

        if self.rect.y < self.target_y: self.rect.y += self.move_speed
        elif self.rect.y > self.target_y: self.rect.y -= self.move_speed

        # --- 2. THE BRAIN: Only acts when we arrive at a grid square ---
        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.behavior_counter += 1
            
            if self.behavior_counter >= 5:
                # Time to hunt!
                self.hunt_player(player_x, player_y)
                self.behavior_counter = 0
            else:
                # Just roaming
                self.roam_randomly()

        self.throw_shurikens()

        # Always update the flying shurikens
        self.update_projectiles()

    def roam_randomly(self):
        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        new_x = self.rect.x + (dx * self.block_size)
        new_y = self.rect.y + (dy * self.block_size)
        self.apply_target_with_boundaries(new_x, new_y)

    def hunt_player(self, player_x, player_y):
        # Figure out if we are further away horizontally or vertically
        diff_x = player_x - self.rect.x
        diff_y = player_y - self.rect.y

        if abs(diff_x) > abs(diff_y):
            # Move on X axis
            step_x = self.block_size if diff_x > 0 else -self.block_size
            self.apply_target_with_boundaries(self.rect.x + step_x, self.rect.y)
        else:
            # Move on Y axis
            step_y = self.block_size if diff_y > 0 else -self.block_size
            self.apply_target_with_boundaries(self.rect.x, self.rect.y + step_y)

    def apply_target_with_boundaries(self, new_x, new_y):
        # This is our safety net so he doesn't walk off screen
        if 0 <= new_x <= self.screen_width - self.boss_size:
            self.target_x = new_x
        if 0 <= new_y <= self.screen_height - self.boss_size:
            self.target_y = new_y


    def throw_shurikens(self):
        current_time = pygame.time.get_ticks()
        
        # 1. The Gatekeeper: Checks if 2 seconds (2000ms) passed
        if current_time - self.last_shot_time > self.shoot_cooldown:


            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                new_shuriken = shuriken.Shuriken(self.rect.centerx, self.rect.centery, dx, dy, self.shuriken_image)
                self.shurikens.append(new_shuriken)

            # 3. CRITICAL: Reset the timer so he has to wait another 2 seconds
            self.last_shot_time = current_time

    def update_projectiles(self):
        for s in self.shurikens:
            s.update()

        self.shurikens = [s for s in self.shurikens if -50 < s.rect.x < self.screen_width + 50
                      and -50 < s.rect.y < self.screen_height + 50]

    def draw_health_bar(self, screen):
        if not self.is_spawning:
            bar_width = 50
            bar_height = 6
            x = self.rect.centerx - (bar_width // 2)
            
            # --- ADAPTIVE POSITIONING ---
            # If the boss is in the top 50 pixels of the screen...
            if self.rect.top < 50:
                # Put the bar 15 pixels BELOW the boss
                y = self.rect.bottom + 15
            else:
                # Put the bar 15 pixels ABOVE the boss (Normal)
                y = self.rect.top - 15
            
            # Calculate health
            # (Assuming 5 is your BOSS_STARTING_HEALTH)
            health_ratio = max(0, self.health / 5)
            current_bar_width = int(bar_width * health_ratio)

            # 1. Background
            pygame.draw.rect(screen, (50, 0, 0), (x, y, bar_width, bar_height))
            # 2. Health (Green/Red)
            color = (0, 255, 0) if health_ratio > 0.4 else (255, 0, 0)
            pygame.draw.rect(screen, color, (x, y, current_bar_width, bar_height))
            
            # 3. SEGMENT MARKERS (The League of Legends lines)
            # Draw a small black line for every unit of health
            for i in range(1, 5): # For 5 HP, we draw 4 internal lines
                marker_x = x + (i * (bar_width // 5))
                pygame.draw.line(screen, (0, 0, 0), (marker_x, y), (marker_x, y + bar_height - 1))

            # 4. Outline
            pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_width, bar_height), 1)

    def flashing_screen(self, screen):
        current_time = pygame.time.get_ticks()

        # --- 1. THE SCREEN FLASH (Intro) ---
        if self.is_spawning:
            # We use a simple toggle: every 200ms, switch between red and normal
            if (current_time // 200) % 2 == 0:
                # Create a transparent red surface the size of the game window
                flash_overlay = pygame.Surface((self.screen_width, self.screen_height))
                flash_overlay.fill((255, 0, 0)) # Pure Red
                flash_overlay.set_alpha(70)     # Low alpha = subtle "glow"
                screen.blit(flash_overlay, (0, 0))
        
