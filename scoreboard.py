import json
import pygame



class Scoreboard:
    def __init__(self, screen_width, screen_height, font_size=30):
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.color = (255, 255, 255)  # white
        self.position = (250, 30)      # top-left corner
        self.screen_width = screen_width
        self.screen_height = screen_height

    def increase(self, points):
        self.score += points

    def reset(self):
        self.score = 0

    def draw(self, screen, snake):
        # Draw score + high score
        score_text = self.font.render(
            f"Score: {self.score} High Score: {self.high_score}",
            True,
            self.color
        )
        screen.blit(score_text, self.position)
        # If paused, draw big "PAUSED" in the center
        if snake.is_paused:
            pause_font = pygame.font.SysFont("Arial", 72, bold=True)
            pause_text = pause_font.render("PAUSED", True, self.color)
            screen.blit(
                pause_text,
                (
                    self.screen_width // 2 - pause_text.get_width() // 2,
                    self.screen_height // 2 - pause_text.get_height() // 2
                )
            )



    def save_high_score(self, score, filename="highscore.json"):
        if self.score > self.high_score:
            data = {"high_score": score}
            with open(filename, "w", encoding="UTF-8") as f:
                json.dump(data, f)
            self.high_score = score
    def load_high_score(self, filename="highscore.json"):
        try:
            with open(filename, "r", encoding="UTF-8") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except FileNotFoundError:
            return 0

