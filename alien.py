import pygame
import random
import shuriken
from sprite import SpriteManager
from path_util import resource_path

class Alien:
    def __init__(self, screen_width, screen_height, level, block_size, hud_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.hud_height = hud_height
        self.boss_alive = True
        self.is_spawning = True
        self.intro_triggered = False
        self.spawn_timer = pygame.time.get_ticks()
        self.max_health = 5
        self.health = self.max_health
        self.block_size = block_size
        self.move_speed = 5
        self.boss_size = block_size * 4
        self.behavior_counter = 0
        self.hit_cooldown = 500
        self.last_hit_time = 0
        self.is_dying = False
        self.death_alpha = 255
        self.death_timer = 0
        self.pattern_index = 0
        self.patterns = [
            [(0, -1), (0, 1)],          # Pattern 0: Vertical (Up/Down)
            [(1, 0), (-1, 0)],          # Pattern 1: Horizontal (Left/Right)
            [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Pattern 2: All 4 (The "Danger" move)
        ]

        # Graphics
        self.image = pygame.image.load(resource_path("assets/alien.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.boss_size, self.boss_size))
        self.image.set_colorkey((0, 0, 0))

        # Projectiles
        sprites = SpriteManager(resource_path("assets/snake2.png"), block_size=self.block_size)
        self.shuriken_image = sprites.get_sprite(col=6, row=6)
        self.shurikens = []
        self.last_shot_time = 0
        self.shoot_cooldown = 2000

        # Position
        self.x = random.randrange(0, screen_width - self.boss_size, block_size)
        self.y = random.randrange(self.hud_height + self.block_size, 
                          self.screen_height - self.boss_size, 
                          self.block_size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.target_x = self.x
        self.target_y = self.y


        self.reset(level)

    def reset(self, level):
        """Call this to restart the boss completely"""
        self.boss_alive = True
        self.is_spawning = True
        self.intro_triggered = False
        self.spawn_timer = pygame.time.get_ticks()
        self.max_health = 5 + (level // 2)  # Set your starting health
        self.health = self.max_health

        self.behavior_counter = 0
        self.last_hit_time = -1000
        self.shurikens = []
        self.last_shot_time = 0
        self.shoot_cooldown = max(800, 2000 - (level * 150))
        self.move_speed = 5 + (level * 2)
        self.is_dying = False
        self.hit_cooldown = 500
        self.death_alpha = 255
        self.death_timer = 0
        self.pattern_index = 0
        self.patterns = [
            [(0, -1), (0, 1)],          # Pattern 0: Vertical (Up/Down)
            [(1, 0), (-1, 0)],          # Pattern 1: Horizontal (Left/Right)
            [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Pattern 2: All 4 (The "Danger" move)
        ]


        # Randomize position
        self.x = random.randrange(0, self.screen_width - self.boss_size, self.block_size)
        self.y = random.randrange(self.hud_height + self.block_size, 
                          self.screen_height - self.boss_size, 
                          self.block_size)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.target_x = self.x
        self.target_y = self.y

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        temp_image = self.image.copy()
        
        # 1. THE DEATH SEQUENCE
        if self.is_dying:
            elapsed = current_time - self.death_timer
            alpha = max(0, 255 - int((elapsed / 1000) * 255))
            temp_image.set_alpha(alpha)
            sink_offset = (elapsed / 1000) * (self.boss_size // 2)
            screen.blit(temp_image, (self.rect.x, self.rect.y + sink_offset))
            if alpha <= 0:
                self.boss_alive = False
            return True

        time_since_hit = current_time - self.last_hit_time

        # 2. THE "HURT" STATE (Takes Priority)
        if time_since_hit < self.hit_cooldown:
            temp_image.set_alpha(120)
            if (current_time // 100) % 2 == 0:
                temp_image.fill((255, 255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                temp_image.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

        # 3. THE "SPAWNING" STATE
        elif self.is_spawning:
            temp_image.set_alpha(150)

        # 4. NEW: THE "WARNING" STATE (Pattern 2)
        # If he is about to fire all 4, give him a golden glow
        elif self.pattern_index == 2:
            temp_image.set_alpha(255)
            # Mix a bit of Yellow (255, 255, 150) into the sprite
            temp_image.fill((255, 255, 150, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
        # 5. THE "NORMAL" STATE
        else:
            temp_image.set_alpha(255)

        # 6. Final render
        screen.blit(temp_image, self.rect)

    def update(self, player_x, player_y):
        current_time = pygame.time.get_ticks()

        # If dying, stop everything (including shurikens)
        if self.is_dying:
            return
        
        # If spawning, we wait. 
        # (Unless you WANT him to slide in, then move the logic below inside here)
        if self.is_spawning:
            if current_time - self.spawn_timer > 1500:
                self.is_spawning = False
            return

        # --- 1. THE LEGS: Sliding with 'Overshoot' protection ---
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y

        # Move X
        if abs(dx) < self.move_speed:
            self.rect.x = self.target_x # Snap to target if we are close
        else:
            self.rect.x += self.move_speed if dx > 0 else -self.move_speed

        # Move Y
        if abs(dy) < self.move_speed:
            self.rect.y = self.target_y # Snap to target if we are close
        else:
            self.rect.y += self.move_speed if dy > 0 else -self.move_speed

        # --- 2. THE BRAIN: Now works perfectly with any speed! ---
        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.behavior_counter += 1
            if self.behavior_counter >= 5:
                # Time to hunt!
                self.hunt_player(player_x, player_y)
                self.behavior_counter = 0
            else:
                # Just roaming
                self.roam_randomly()

        # --- 3. COMBAT ---
        self.throw_shurikens()
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
        # This 'clamps' the X between 0 and the Right Edge
        # It says: "Pick the higher of 0 or the coordinate, but don't let it exceed the max width"
        self.target_x = max(0, min(new_x, self.screen_width - self.boss_size))
        
        # This 'clamps' the Y between 0 and the Bottom Edge
        self.target_y = max(self.hud_height, min(new_y, self.screen_height - self.boss_size))


    def throw_shurikens(self):
        current_time = pygame.time.get_ticks()

        # 1. Check if the boss is ready to shoot
        if current_time - self.last_shot_time > self.shoot_cooldown:

            # 2. Get the current set of directions from our pattern list
            current_directions = self.patterns[self.pattern_index]

            # 3. Spawn the shurikens based on the selected pattern
            for dx, dy in current_directions:
                new_shuriken = shuriken.Shuriken(
                    self.rect.centerx,
                    self.rect.centery,
                    dx, dy,
                    self.shuriken_image
                )
                self.shurikens.append(new_shuriken)

            # 4. Cycle to the next pattern (0 -> 1 -> 2 -> back to 0)
            self.pattern_index = (self.pattern_index + 1) % len(self.patterns)

            # 5. Reset the cooldown timer
            self.last_shot_time = current_time

    def update_projectiles(self):
        for s in self.shurikens:
            s.update()

        self.shurikens = [s for s in self.shurikens if 
                  -50 < s.rect.x < self.screen_width + 50 and 
                  self.hud_height < s.rect.y < self.screen_height + 50]

    def draw_health_bar(self, screen):
        if not self.is_spawning and not self.is_dying:
            bar_width = 50
            bar_height = 6
            safe_zone = self.hud_height + self.block_size
            x = self.rect.centerx - (bar_width // 2)
            
            # --- ADAPTIVE POSITIONING ---
            if self.rect.top < safe_zone:
                y = self.rect.bottom + 15
            else:
                y = self.rect.top - 15
            
            # --- 1. DYNAMIC CALCULATION ---
            # No more hardcoded '5'! 
            health_ratio = max(0, self.health / self.max_health)
            current_bar_width = int(bar_width * health_ratio)

            # Draw Background
            pygame.draw.rect(screen, (50, 0, 0), (x, y, bar_width, bar_height))
            
            # Draw Health (Green/Red)
            color = (0, 255, 0) if health_ratio > 0.4 else (255, 0, 0)
            pygame.draw.rect(screen, color, (x, y, current_bar_width, bar_height))
            
            # --- 2. THE DYNAMIC MARKERS ---
            # We draw a line for every unit of health EXCEPT the very last one
            for i in range(1, self.max_health): 
                # Calculate marker position based on current max_health
                marker_x = x + (i * (bar_width / self.max_health))
                pygame.draw.line(screen, (0, 0, 0), (int(marker_x), y), (int(marker_x), y + bar_height - 1))

            # Draw Outline
            pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_width, bar_height), 1)

    def flashing_screen(self, screen):
        current_time = pygame.time.get_ticks()

        # Calculate how long since we started spawning
        # (Assuming self.spawn_timer was set to pygame.time.get_ticks() in the loop)
        elapsed = current_time - self.spawn_timer

        # --- 1. THE SCREEN FLASH (Intro) ---
        if elapsed < 1500: # Flash for 1.5 seconds
            if (current_time // 200) % 2 == 0:
                play_area_height = self.screen_height - self.hud_height
                flash_overlay = pygame.Surface((self.screen_width, play_area_height))
                flash_overlay.fill((255, 0, 0))
                flash_overlay.set_alpha(70) 
                screen.blit(flash_overlay, (0, self.hud_height))
        else:
            self.is_spawning = False # Turn off the "spawning" state once time is up        

    def take_damage(self, current_time):
        if current_time - self.last_hit_time > self.hit_cooldown and not self.is_dying:
            self.health -= 1
            self.last_hit_time = current_time
            
            # Check for Death
            if self.health <= 0:
                self.is_dying = True
                self.death_timer = current_time
                # Return a special value or just handle sounds inside here
                return "KILLED"

            # Teleport if still alive
            pot_x = random.randint(1, (self.screen_width // self.block_size) - 2) * self.block_size
            min_grid_y = (self.hud_height // self.block_size) + 1
            max_grid_y = (self.screen_height // self.block_size) - 2
            pot_y = random.randint(min_grid_y, max_grid_y) * self.block_size
            self.apply_target_with_boundaries(pot_x, pot_y)
            self.rect.x = self.target_x
            self.rect.y = self.target_y

            return "HIT"
        return "COOLDOWN"
