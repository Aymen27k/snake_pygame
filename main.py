import pygame
import random
from snake import Snake
from food import Food
from walls import Walls
from hud import HUD
from background import Background
from alien import Alien
from projectile import PoisonProjectile
from soundmanager import SoundManager
from musicmanager import MusicManager

#Config
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 660
HUD_HEIGHT = 60
NO_HUD = 0
BLOCK_SIZE = 20
ALIEN_WIDTH = 5
direction= "RIGHT"
running = True
playing = False
menu_choice = None
game_state = "menu"
game_mode = None
game_start_time = 0
total_paused_time = 0
pause_start_tick = 0
boss_active = False
boss_killed = 0
boss_milestones = [30, 60, 90, 120, 150, 190, 250, 300, 400, 500]
projectiles = []
next_goal = 0
LAST_SPEED = 10

# Menu snake specific rule
MENU_SNAKE_MAX_LENGTH = SCREEN_WIDTH // BLOCK_SIZE // 2




#initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game | Made by AYMEN")
clock = pygame.time.Clock()
player_snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT)
food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, player_snake.segments, HUD_HEIGHT)
walls = Walls(SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT)
hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT, game_mode)
bg = Background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT)
game_over_bg = Background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT, bg_path="assets/snake_game_over.png")
new_high_score_bg = Background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT, bg_path="assets/new_high_score.png")
menu_snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT)
alien_boss = Alien(SCREEN_WIDTH, SCREEN_HEIGHT, boss_killed, BLOCK_SIZE, HUD_HEIGHT)
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
        bg.draw(is_menu=True)
        walls.draw(screen, mode="wrap", y_offset=NO_HUD)
        menu_snake.move_auto(screen)
        walls.check_collision(menu_snake, SCREEN_WIDTH, SCREEN_HEIGHT, mode="wrap", override_hud=NO_HUD)

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

    seconds_passed = 0 
    paused_ticks = 0 
    typing = is_new_high_score
    player_name = ""

    while continue_game:
        if not typing:
            seconds_passed = (pygame.time.get_ticks() - start_ticks - paused_ticks) // 1000
        else:
            paused_ticks = pygame.time.get_ticks() - start_ticks - (seconds_passed * 1000)

        remaining = countdown_time - seconds_passed
        screen.fill((0,0,0))

        if is_new_high_score:
            new_high_score_bg.draw(is_menu=True)
        else:
            game_over_bg.draw(is_menu=True)
        # Create a small "Summary Box" on the screen
        stats_font = pygame.font.SysFont("Courier New", 28, bold=True) # Courier looks 'techy'

        left_x = SCREEN_WIDTH // 2 - 180
        right_x = SCREEN_WIDTH // 2 + 50
        stats_y = SCREEN_HEIGHT // 2 + 150

        # Render the lines
        score_text = stats_font.render(f"SCORE: {hud.score}", True, (0, 255, 0))
        time_text = stats_font.render(f"TIME : {time_str}", True, (255, 255, 255))
        boss_text = stats_font.render(f"BOSSES: {boss_kills}", True, (0, 0, 0))
        # Draw them with a bit of vertical spacing
        screen.blit(score_text, (left_x, stats_y))
        screen.blit(time_text, (right_x, stats_y))
        screen.blit(boss_text, (SCREEN_WIDTH // 2 - 60, stats_y + 70))
        # Flashing "Press Enter"
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            prompt = font.render("Press ENTER to Continue", True, (255, 255, 255))
            screen.blit(prompt,(screen.get_width() // 2 - prompt.get_width() // 2, screen.get_height()//2 + 50))

        if typing:
            # Draw Name Input Box
            input_label = font.render("NEW RECORD! ENTER NAME:", True, (255, 215, 0))
            name_text = font.render(player_name + ("_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""), True, (255, 255, 255))

            screen.blit(input_label, (SCREEN_WIDTH//2 - input_label.get_width()//2, SCREEN_HEIGHT//2 - 100))
            screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        else:
            # Draw normal Continue
            text = font.render(f"Continue? {remaining}", True, (255,255,255))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(player_name) > 0:
                        typing = False # Finish typing [cite: 2024-12-19]
                        # Save it now! [cite: 2024-12-19]
                        hud.save_high_score(hud.score, player_name, hud.game_mode)
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        # Limit name to 8 characters for that arcade feel [cite: 2024-12-19]
                        if len(player_name) < 8 and event.unicode.isalnum():
                            player_name += event.unicode.upper()
            else:
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
    global game_start_time, boss_killed, total_paused_time, pause_start_tick, boss_active, boss_milestones
    total_paused_time = 0
    pause_start_tick = 0
    game_start_time = pygame.time.get_ticks()
    boss_milestones = [30, 60, 90, 120, 150, 190, 250, 300, 400, 500]
    player_snake.create_snake()
    food.refresh(player_snake.segments)
    alien_boss.reset(boss_killed)
    boss_active = False
    boss_killed = 0
    player_snake.poison_ammo = 0
    hud.reset()
    sounds.stop("game_over")
    music.stop()
    music.play("gameplay")

def handle_boss_death():
    global boss_killed
    boss_killed += 1
    music.stop()
    sounds.play("scream")
    sounds.play("explosion")


def is_game_over(player_snake, walls, alien_boss, game_mode, current_score):
    # 1. Self Collision
    if player_snake.check_self_collision():
        return True
    
    # 2. Wall Collision
    if walls.check_collision(player_snake, SCREEN_WIDTH, SCREEN_HEIGHT, game_mode):
        return True
        
    # 3. Boss Body Collision
    if boss_active and alien_boss.boss_alive:
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
        menu_choice = menu(screen, hud.font, player_snake)
        if menu_choice in ("classic","wrap"):
            game_mode = menu_choice
            hud.set_mode(game_mode)
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
                boss_active = False
                boss_killed = 0
                total_paused_time = 0
                pause_start_tick = 0
                player_snake.poison_ammo = 0
                boss_milestones = [30, 60, 90, 120, 150, 190, 250, 300, 400, 500]
                player_snake.create_snake()
                food.reset_poison()
                alien_boss.reset(boss_killed)
                hud.reset()
                game_start_time = pygame.time.get_ticks()
                direction = "RIGHT"
            elif game_state == "resume":
                # Resume existing game
                if boss_active and alien_boss.boss_alive and not alien_boss.is_dying:
                    music.play("ultra")
                music.play("gameplay")
            player_snake.is_paused = False

            playing = True


            while playing:
                # Check IF the list is empty BEFORE trying to grab the first number
                if boss_milestones:
                    next_goal = boss_milestones[0]

                    # Now check the score
                    if hud.score >= next_goal:
                        if not boss_active:
                            boss_active = True
                            boss_milestones.pop(0)
                            print(f"Boss {boss_killed + 1} Triggered!")
                            print(f"DEBUG: Boss #{boss_killed} spawned with Speed: {alien_boss.move_speed}, HP: {alien_boss.health} Fire rate: {alien_boss.shoot_cooldown}")
                else:
                    # Optional: If the list IS empty, give it a new goal!
                    # This makes the game infinite.
                    boss_milestones.append(hud.score + 50)
                game_speed = min(10 + (hud.score // 10), 20)
                if game_speed > LAST_SPEED:
                    sounds.play("speed_up")
                    LAST_SPEED = game_speed
                if boss_active and alien_boss.boss_alive and not alien_boss.is_dying:
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
                            if player_snake.is_paused:
                                # Just entered pause: record the "start" of the pause
                                pause_start_tick = pygame.time.get_ticks()
                            else:
                                # Just exited pause: calculate duration and add to buffer
                                pause_duration = pygame.time.get_ticks() - pause_start_tick
                                total_paused_time += pause_duration
                        elif event.key == pygame.K_ESCAPE:
                            if not player_snake.is_paused:
                                player_snake.is_paused = True
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
                            elif event.key == pygame.K_b: # Press 'B' for Boss
                                hud.score += 10
                                print("Score cheat detected ! You gain 10 points")
                            elif event.key == pygame.K_SPACE and player_snake.poison_ammo > 0:
                                # Create a new shot at the snake's head position
                                new_shot = PoisonProjectile(player_snake.head.x, player_snake.head.y, direction)
                                projectiles.append(new_shot)
                                player_snake.poison_ammo -= 1
                                sounds.play("shoot")
                # 2. Update game state
                if not player_snake.is_paused:
                    if boss_active and alien_boss.boss_alive:
                        alien_boss.update(player_snake.head.x, player_snake.head.y)
                        alien_boss.update_projectiles()
                    old_head_rect = player_snake.head.copy()
                    player_snake.move(direction)
                    if player_snake.head.colliderect(food.rect) or old_head_rect.colliderect(food.rect):
                        sounds.play("eat")
                        hud.increase(food.value)
                        food.refresh(player_snake.segments)
                        player_snake.should_grow = True
                    if food.poison_active:
                        if player_snake.head.colliderect(food.poison_rect) or old_head_rect.colliderect(food.poison_rect):
                            food.poison_active = False
                            food.last_expiry_time = pygame.time.get_ticks()
                            player_snake.poison_ammo += 1
                            sounds.play("poison_get")
                            food.poison_rect.x = -100
                            food.poison_rect.y = -100

                # Fighting the Alien Boss
                if boss_active:
                    boss_hitbox = alien_boss.rect.inflate(-30, -30)
                    current_time = pygame.time.get_ticks() # Use this for everything!

                    # Poison food logic
                    if not food.poison_active:
                        # 1. Cooldown: Only spawn if it's been 3 seconds since the last one died
                        # We'll need to initialize food.last_expiry_time = 0 in your Food __init__
                        if current_time - getattr(food, 'last_expiry_time', 0) > 3000:
                            # 2. Random Chance: 1% chance per frame
                            if random.random() < 0.01:
                                food.spawn_poison(player_snake.segments)
                                print("Poison food spawned")
                    else:
                        if not player_snake.is_paused:
                            # 3. Expiry: Use the same current_time here
                            if current_time - food.spawn_time > food.duration:
                                food.poison_active = False
                                food.poison_rect.topleft = (-100, -100)
                                food.last_expiry_time = current_time # Set the cooldown start
                                print("Poison food expired")

                    # 1. TRIGGER DEATH (Only when touching)
                    if player_snake.head.colliderect(boss_hitbox) and alien_boss.health > 0 and not alien_boss.is_spawning:
                        result = alien_boss.take_damage(current_time)
                        if result == "HIT":
                            sounds.play("dmg")

                            if len(player_snake.segments) > 5:
                                for _ in range(3):
                                    player_snake.segments.pop()
                        elif result == "KILLED":
                            handle_boss_death()

                    # This must be indented at the same level as "if boss_active"
                    if alien_boss.is_dying:
                        if pygame.time.get_ticks() - alien_boss.death_timer > 2000:
                            boss_active = False
                            alien_boss.is_dying = False
                            alien_boss.intro_triggered = False
                            alien_boss.boss_alive = False
                            alien_boss.shurikens.clear()
                            projectiles.clear()
                            alien_boss.reset(boss_killed) # Important to reset for next wave!
                            print(f"CLEANUP COMPLETE! Ready for next milestone. Boss status: {boss_active}")
                    #print(f"VICTORY! The Alien has retreated!")
                    # Inside your main loop (Update Section)
                    for s in alien_boss.shurikens[:]:
                        if player_snake.head.colliderect(s.rect):
                            # 1. The Penalty: Remove the tail
                            # 3. Feedback (Optional but recommended)
                            #print("OUCH! Snake Shrunk!")
                            if len(player_snake.segments) > 2 and not alien_boss.is_dying:
                                sounds.play("dmg")
                                player_snake.segments.pop()
                                # 2. Cleanup: Remove the shuriken that hit us
                                alien_boss.shurikens.remove(s)
                    # Update projectiles
                    for p in projectiles[:]:  # Using [:] creates a copy so we can remove items safely
                        p.update()
                        if p.rect.colliderect(boss_hitbox):
                            result = alien_boss.take_damage(current_time)
                            if result == "HIT":
                                projectiles.remove(p)
                                sounds.play("dmg")
                            elif result == "KILLED":
                                projectiles.remove(p)
                                handle_boss_death()
                        if not p.active:
                            projectiles.remove(p)

                # Game Over
                if is_game_over(player_snake, walls, alien_boss, game_mode, hud.score):
                    # Calculate total seconds
                    end_time = pygame.time.get_ticks()
                    actual_play_ms = (end_time - game_start_time) - total_paused_time
                    total_seconds = actual_play_ms // 1000
                    # Format it into Minutes:Seconds
                    minutes = total_seconds // 60
                    seconds = total_seconds % 60
                    time_string = f"{minutes:02d}:{seconds:02d}"


                    new_record = hud.is_new_high_score()


                    music.play("game_over", loop=0)
                    sounds.play("game_over")
                    # Continue ?
                    if continue_screen(screen, hud.font, new_record, time_string, boss_killed):
                        reset_game()
                        direction = "RIGHT"
                    else:
                        playing = False
                        game_state = "menu"




                # 3. Render
                screen.fill((0, 0, 0))
                bg.draw()
                walls.draw(screen, game_mode)
                food.draw(screen, player_snake)
                player_snake.draw(screen, direction)
                hud.draw(screen, player_snake, HUD_HEIGHT, boss_killed)
                if boss_active:
                    if not alien_boss.intro_triggered:
                        alien_boss.spawn_timer = pygame.time.get_ticks()
                        alien_boss.intro_triggered = True
                        alien_boss.is_spawning = True
                    alien_boss.flashing_screen(screen)
                if boss_active and alien_boss.boss_alive:
                    alien_boss.draw(screen)
                    alien_boss.draw_health_bar(screen)
                    # Draw a red outline around the boss's actual hitbox so you can see it
                    #pygame.draw.rect(screen, (255, 0, 0), alien_boss.rect.inflate(-30, -30), 2)
                    for s in alien_boss.shurikens:
                        s.draw(screen)
                    for p in projectiles:
                        p.draw(screen)
                pygame.display.update()

                # 4. Control speed
                clock.tick(game_speed)


pygame.quit()