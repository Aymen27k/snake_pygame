import pygame
import random
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
game_start_time = 0
boss_killed = 0
BOSS_TRIGGER_SCORE = 10

# Menu snake specific rule
MENU_SNAKE_MAX_LENGTH = SCREEN_WIDTH // BLOCK_SIZE // 2
LAST_SPEED = 10



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
new_high_score_bg = Background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, bg_path="assets/new_high_score.png")
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
def continue_screen(screen, font, is_new_high_score, time_str, boss_kills, countdown_time=10):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    start_ticks = pygame.time.get_ticks()
    continue_game = True
    player_chose = False
    while continue_game:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining = countdown_time - seconds_passed

        screen.fill((0,0,0))

        if is_new_high_score:
            new_high_score_bg.draw()
        else:
            game_over_bg.draw()
        # Create a small "Summary Box" on the screen
        stats_font = pygame.font.SysFont("Courier New", 28, bold=True) # Courier looks 'techy'

        left_x = SCREEN_WIDTH // 2 - 180
        right_x = SCREEN_WIDTH // 2 + 50
        stats_y = SCREEN_HEIGHT // 2 + 150

        # Render the lines
        score_text = stats_font.render(f"SCORE: {score.score}", True, (0, 255, 0))
        time_text = stats_font.render(f"TIME : {time_str}", True, (255, 255, 255))
        boss_text = stats_font.render(f"BOSSES: {boss_kills}", True, (0, 0, 0))
        # Draw them with a bit of vertical spacing
        screen.blit(score_text, (left_x, stats_y))
        screen.blit(time_text, (right_x, stats_y))
        screen.blit(boss_text, (SCREEN_WIDTH // 2 - 60, stats_y + 70))
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
    global game_start_time, boss_killed
    game_start_time = pygame.time.get_ticks()
    player_snake.create_snake()
    food.refresh(player_snake.segments)
    alien_boss.reset()
    boss_killed = 0
    score.reset()
    sounds.stop("game_over")
    music.stop()
    music.play("gameplay")


def is_game_over(player_snake, walls, alien_boss, game_mode, current_score):
    # 1. Self Collision
    if player_snake.check_self_collision():
        return True
    
    # 2. Wall Collision
    if walls.check_collision(player_snake, SCREEN_WIDTH, SCREEN_HEIGHT, game_mode):
        return True
        
    # 3. Boss Body Collision
    if current_score >= BOSS_TRIGGER_SCORE:
        boss_hitbox = alien_boss.rect.inflate(-30, -30)
        if player_snake.head.colliderect(boss_hitbox):
            pass

    # 4. NEW: Shuriken Death (When snake has no more segments)
    # We check if the snake is just a head and was hit by a projectile
    # (This assumes you handle the shrinking elsewhere, and this just checks the final blow)
    if len(player_snake.segments) < 3:
        # You could add a flag here like self.is_dead
        # or just return True if your shrinking logic sets a specific state
        return True

    return False

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
                alien_boss.reset()
                score.reset()
                game_start_time = pygame.time.get_ticks()
                print(f"Game start time post Entry point = {game_start_time}")
                direction = "RIGHT"
            elif game_state == "resume":
                # Resume existing game
                if score.score >= BOSS_TRIGGER_SCORE and alien_boss.boss_alive and not alien_boss.is_dying:
                    music.play("ultra")
                music.play("gameplay")
            player_snake.is_paused = False

            playing = True


            while playing:
                game_speed = min(10 + (score.score // 5), 20)
                if game_speed > LAST_SPEED:
                    sounds.play("speed_up")
                    LAST_SPEED = game_speed
                if score.score >= BOSS_TRIGGER_SCORE and alien_boss.boss_alive and not alien_boss.is_dying:
                    music.play("ultra")
                else:
                    music.play("gameplay")
                # 1. Handle input/events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        playing = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        # 1. These keys should ALWAYS work (Pause/Exit)
                        if event.key == pygame.K_p:
                            player_snake.is_paused = not player_snake.is_paused
                        elif event.key == pygame.K_ESCAPE:
                            game_state = "menu"
                            playing = False

                        # 2. THE FIX: Only update direction if NOT paused
                        if not player_snake.is_paused:
                            if event.key == pygame.K_UP and direction != "DOWN":
                                direction = "UP"
                            elif event.key == pygame.K_DOWN and direction != "UP":
                                direction = "DOWN"
                            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                                direction = "LEFT"
                            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                                direction = "RIGHT"
                # 2. Update game state
                if not player_snake.is_paused:
                    if score.score >= BOSS_TRIGGER_SCORE and alien_boss.boss_alive:
                        alien_boss.update(player_snake.head.x, player_snake.head.y)
                        alien_boss.update_projectiles()
                    old_head_rect = player_snake.head.copy()
                    player_snake.move(direction)
                    if player_snake.head.colliderect(food.rect) or old_head_rect.colliderect(food.rect):
                        sounds.play("eat")
                        score.increase(food.value)
                        food.refresh(player_snake.segments)
                        player_snake.should_grow = True

                # Fighting the Alien Boss
                if score.score >= BOSS_TRIGGER_SCORE and alien_boss.boss_alive:
                    boss_hitbox = alien_boss.rect.inflate(-30, -30)
                    current_time = pygame.time.get_ticks()
                    if player_snake.head.colliderect(boss_hitbox) and alien_boss.health > 0 and current_time - alien_boss.last_hit_time > alien_boss.hit_cooldown:
                        alien_boss.health -= 1
                        alien_boss.last_hit_time = current_time
                        sounds.play("boss_dmg")
                        if alien_boss.health > 0:
                            new_x = random.randint(1, (SCREEN_WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
                            new_y = random.randint(1, (SCREEN_HEIGHT // BLOCK_SIZE) - 2) * BLOCK_SIZE

                            alien_boss.rect.x = new_x
                            alien_boss.rect.y = new_y
                            alien_boss.target_x = new_x
                            alien_boss.target_y = new_y

                            if len(player_snake.segments) > 5:
                                for _ in range(3):
                                    player_snake.segments.pop()
                        #print(f"BOSS HIT! Health remaining: {alien_boss.health}")
                        if alien_boss.health <= 0 and not alien_boss.is_dying:
                            alien_boss.is_dying = True
                            alien_boss.death_timer = pygame.time.get_ticks()
                            boss_killed += 1
                            music.stop()
                            sounds.play("scream")
                            sounds.play("explosion")
                            #print("VICTORY! The Alien has retreated!")
                    # Inside your main loop (Update Section)
                    for s in alien_boss.shurikens[:]:
                        if player_snake.head.colliderect(s.rect):
                            # 1. The Penalty: Remove the tail
                            # 3. Feedback (Optional but recommended)
                            #print("OUCH! Snake Shrunk!")
                            if len(player_snake.segments) > 2:
                                sounds.play("dmg")
                                player_snake.segments.pop()
                                # 2. Cleanup: Remove the shuriken that hit us
                                alien_boss.shurikens.remove(s)

                # Game Over
                if is_game_over(player_snake, walls, alien_boss, game_mode, score.score):
                    # Calculate total seconds
                    end_time = pygame.time.get_ticks()
                    total_seconds = (end_time - game_start_time) // 1000
                    # Format it into Minutes:Seconds
                    minutes = total_seconds // 60
                    seconds = total_seconds % 60
                    time_string = f"{minutes:02d}:{seconds:02d}"


                    new_record = score.is_new_high_score()
                    if new_record:
                        score.save_high_score(score.score, game_mode)

                    music.play("game_over", loop=0)
                    sounds.play("game_over")
                    # Continue ?
                    if continue_screen(screen, score.font, new_record, time_string, boss_killed):
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
                if score.score >= BOSS_TRIGGER_SCORE:
                    if not alien_boss.intro_triggered:
                        alien_boss.spawn_timer = pygame.time.get_ticks() # Start the 1.5s clock NOW
                        alien_boss.intro_triggered = True
                    alien_boss.flashing_screen(screen)
                if score.score >= BOSS_TRIGGER_SCORE and alien_boss.boss_alive:
                    alien_boss.draw(screen)
                    alien_boss.draw_health_bar(screen)
                    # Draw a red outline around the boss's actual hitbox so you can see it
                    pygame.draw.rect(screen, (255, 0, 0), alien_boss.rect.inflate(-30, -30), 2)
                    for s in alien_boss.shurikens:
                        s.draw(screen)
                pygame.display.update()

                # 4. Control speed
                clock.tick(game_speed)


pygame.quit()