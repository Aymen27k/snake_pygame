import json
import pygame
from sprite import SpriteManager

class HUD:
    def __init__(self, screen_width, screen_height, font_size=30):
        self.score = 0
        self.high_score = 0
        self.high_score_name = "---"
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.color = (255, 255, 255)  # white
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Highscore Medal Icon
        self.medal_icon = pygame.image.load("./assets/medal.png").convert_alpha()
        self.medal_icon = pygame.transform.scale(self.medal_icon, (35, 35))
        # Thunder speed Icon
        self.thunder_icon = pygame.image.load("./assets/speed.png").convert_alpha()
        self.thunder_icon = pygame.transform.scale(self.thunder_icon, (20, 20))
        # Dead Alien Icon
        self.dead_alien = pygame.image.load("./assets/dead_alien2.png").convert_alpha()
        self.dead_alien = pygame.transform.scale(self.dead_alien, (35, 35))


    def increase(self, points):
        self.score += points

    def reset(self):
        self.score = 0

    def draw(self, screen, snake, HUD_HEIGHT, boss_killed):
        # 1. Color logic (Gold if beating record)
        display_color = (255, 215, 0) if self.score > self.high_score else self.color
        
        # 2. Draw HUD Background
        pygame.draw.rect(screen, (15, 15, 15), (0, 0, self.screen_width, HUD_HEIGHT))
        pygame.draw.line(screen, (60, 60, 60), (0, HUD_HEIGHT), (self.screen_width, HUD_HEIGHT), 2)

        # 3. Render surfaces (Now including the Name)
        score_surf = self.font.render(f"Score: {self.score}", True, display_color)
        # Combine the Name and the Score number
        high_score_text = f"{self.high_score_name}: {self.high_score}"
        high_val_surf = self.font.render(high_score_text, True, (255, 215, 0))

        # 4. Calculate Total Width for perfect centering
        gap = 15
        medal_w = self.medal_icon.get_width()
        total_width = score_surf.get_width() + gap + medal_w + gap + high_val_surf.get_width()
        
        current_x = (self.screen_width - total_width) // 2
        y_center = HUD_HEIGHT // 2

        # 5. Draw everything
        # Current Score
        screen.blit(score_surf, (current_x, y_center - score_surf.get_height() // 2))
        current_x += score_surf.get_width() + gap
        
        # Medal
        screen.blit(self.medal_icon, (current_x, y_center - medal_w // 2))
        current_x += medal_w + gap
        
        # High Score Name + Number (e.g., "AYMEN 256") [cite: 2024-12-19, 2026-02-06]
        screen.blit(high_val_surf, (current_x, y_center - high_val_surf.get_height() // 2))

        # If paused, draw big "PAUSED" in the center
        if snake.is_paused:
            # --- THE BLINK TRIGGER ---
            # Only draw the text if the current half-second is 'even'
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                pause_font = pygame.font.SysFont("Arial", 72, bold=True)
                pause_text = pause_font.render("PAUSED", True, self.color)
                screen.blit(
                    pause_text,
                    (
                        self.screen_width // 2 - pause_text.get_width() // 2,
                        self.screen_height // 2 - pause_text.get_height() // 2
                    )
                )
        for i in range(snake.poison_ammo):
            # Calculate horizontal spacing
            icon_x = 30 + (i * 25)
            icon_y = HUD_HEIGHT // 2

            # Draw a small purple circle or use a sprite if you passed it in
            pygame.draw.circle(screen, (128, 0, 128), (icon_x, icon_y), 7)
            # Optional: Add a small white "shine" to the ammo icon
            pygame.draw.circle(screen, (200, 100, 255), (icon_x - 2, icon_y - 2), 2)

        # SpeedMeter
        # In your draw method:
        speed_level = self.score // 10  # How many thunder bolts are "earned"

        for i in range(10):  # Draw 10 icons
            icon_x = (self.screen_width - 40) - (i * 15)
            icon_y = HUD_HEIGHT // 4

            if (9 - i) < speed_level:
                self.thunder_icon.set_alpha(255)  # Earned: Solid [cite: 2024-12-19]
            else:
                self.thunder_icon.set_alpha(50)
                
            screen.blit(self.thunder_icon, (icon_x, icon_y - self.thunder_icon.get_height() // 2))

            # Boss Kills (Bottom Tier)
            if boss_killed != 0:
                icon_y_boss = HUD_HEIGHT * 3 // 4
                boss_text = self.font.render(f"x {boss_killed}", True, (255, 255, 255))

                # Anchor it to the right, same as the thunder bolts
                screen.blit(self.dead_alien, (self.screen_width - 120, icon_y_boss - self.dead_alien.get_height() // 2))
                screen.blit(boss_text, (self.screen_width - 90, icon_y_boss - boss_text.get_height() // 2))

    def is_new_high_score(self):
        """Returns True if the current session score is strictly greater than the record."""
        # We compare against self.high_score which was set during load_high_score()
        return self.score > self.high_score
