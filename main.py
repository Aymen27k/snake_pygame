import pygame
from snake import Snake
from food import Food
from walls import Walls
from scoreboard import Scoreboard
from background import Background
from alien import Alien
from soundmanager import SoundManager
from musicmanager import MusicManager

#Config
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
ALIEN_WIDTH = 5
direction= "RIGHT"
running = True
playing = False
menu_choice = None
game_state = "menu"
game_mode = None
# Menu snake specific rule
MENU_SNAKE_MAX_LENGTH = SCREEN_WIDTH // BLOCK_SIZE // 2
last_speed = 10


#initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game | Made by AYMEN")
clock = pygame.time.Clock()
player_snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, player_snake.segments)
walls = Walls(SCREEN_WIDTH, SCREEN_HEIGHT)
score = Scoreboard(SCREEN_WIDTH, SCREEN_HEIGHT, game_mode)
bg = Background(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
game_over_bg = Background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, bg_path="assets/snake_game_over.png")
menu_snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
alien_boss = Alien(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
sounds = SoundManager()
music = MusicManager()


# Main Menu
def menu(screen, font, player_snake):
    options = []
    if player_snake.is_paused:
        options.append("Resume")
    options.extend(["Classic Mode (walls kill)", "Wrap-around Mode (teleport)", "Exit"])
    selected = 0
    menu_snake.max_snake_length = MENU_SNAKE_MAX_LENGTH
    menu_snake.create_snake()
    music.play("menu")
    while running:
        # Menu rendering
        screen.fill((0,0,0))
        bg.draw()
        walls.draw(screen, "wrap")
        menu_snake.move_auto(screen)
        walls.check_collision(menu_snake, SCREEN_WIDTH, SCREEN_HEIGHT, "wrap")

        # Draw title
        title = font.render("Snake Game Menu", True, (255,255,255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))

        # Draw options
        for i, option in enumerate(options):
            color = (255,255,0) if i == selected else (255,255,255)
            text = font.render(option, True, color)
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 200 + i*50))

        pygame.display.update()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    choice = options[selected]
                    if choice == "Resume":
                        return "resume"
                    elif choice.startswith("Classic"):
                        return "classic"
                    elif choice.startswith("Wrap"):
                        return "wrap"
                    else:
                        return "exit"


# Continue Screen
def continue_screen(screen, font, countdown_time=10):

    start_ticks = pygame.time.get_ticks()
    continue_game = True
    player_chose = False
    while continue_game:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining = countdown_time - seconds_passed

        screen.fill((0,0,0))
        game_over_bg.draw()
        # Countdown Text
        text = font.render(f"Continue? {remaining}", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2,
                           screen.get_height()//2 - text.get_height()//2))
        # Flashing "Press Enter"
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            prompt = font.render("Press ENTER to Continue", True, (255, 255, 255))
            screen.blit(prompt,(screen.get_width() // 2 - prompt.get_width() // 2, screen.get_height()//2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # player continues
                    player_chose = True
                    continue_game = False
                elif event.key == pygame.K_ESCAPE:
                    music.play("menu")
                    continue_game = False
                    player_chose = False

        if remaining <= 0:
            continue_game = False

    return player_chose

def reset_game():
    player_snake.create_snake()
    food.refresh(player_snake.segments)
    score.reset()
    sounds.stop("game_over")
    music.stop()
    music.play("gameplay")

while running:
    if game_state == "menu":
        menu_choice = menu(screen, score.font, player_snake)
        if menu_choice in ("classic","wrap"):
            game_mode = menu_choice
            score.set_mode(game_mode)
            game_state = "playing"
        elif menu_choice == "exit":
            game_state = "exit"
            break
        elif menu_choice == "resume":
            game_state = "resume"

        if game_state in ("playing", "resume"):
            if game_state == "playing":
                music.play("gameplay")
                # Entry Point (Game reset)
                player_snake.is_paused = False
                player_snake.create_snake()
                score.reset()
                direction = "RIGHT"
            elif game_state == "resume":
                # Resume existing game
                if score.score >= 20:
                    music.play("ultra")
                music.play("gameplay")
            player_snake.is_paused = False

            playing = True


            while playing:
                game_speed = min(10 + (score.score // 5), 20)
                if game_speed > last_speed:
                    sounds.play("speed_up")
                    last_speed = game_speed
                if score.score >= 20:
                    music.play("ultra")
                # 1. Handle input/events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or game_state == "exit":
                        playing = False
                        running = False
                        game_state = "exit"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and direction != "DOWN":
                            direction = "UP"
                        elif event.key == pygame.K_DOWN and direction != "UP":
                            direction = "DOWN"
                        elif event.key == pygame.K_LEFT and direction != "RIGHT":
                            direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and direction != "LEFT":
                            direction = "RIGHT"
                        elif event.key == pygame.K_p:
                            player_snake.is_paused = not player_snake.is_paused
                        elif event.key == pygame.K_ESCAPE:
                            if not player_snake.is_paused:
                                player_snake.is_paused = not player_snake.is_paused
                            game_state = "menu"
                            playing = False
            
                # 2. Update game state
                if not player_snake.is_paused:
                    alien_boss.update()
                    old_head_rect = player_snake.head.copy()
                    player_snake.move(direction)
                    if player_snake.head.colliderect(food.rect) or old_head_rect.colliderect(food.rect):
                        sounds.play("eat")
                        score.increase(food.value)
                        food.refresh(player_snake.segments)
                        player_snake.should_grow = True

                #Game Over
                if player_snake.check_self_collision() or walls.check_collision(player_snake, SCREEN_WIDTH, SCREEN_HEIGHT, game_mode):
                    score.save_high_score(score.score, game_mode)
                    music.play("game_over", loop=0)
                    sounds.play("game_over")
                    if continue_screen(screen, score.font):
                        reset_game()
                        direction = "RIGHT"
                    else:
                        print("Returning to Menu...")
                        playing = False
                        game_state = "menu"




                # 3. Render
                screen.fill((0, 0, 0))
                bg.draw()
                walls.draw(screen, game_mode)
                food.draw(screen, player_snake)
                player_snake.draw(screen, direction)
                score.draw(screen, player_snake)
                alien_boss.draw(screen)
                pygame.display.update()

                # 4. Control speed
                clock.tick(game_speed)


pygame.quit()