import pygame
from config import *
from player import Player
from obstacle import Obstacle
from powerup import PowerUp
from scores import load_top_scores, save_score

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Player Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 72)

# Challenge 9: best score of this execution. It is NOT reset when a new game starts.
high_score = 0

# Game states: "menu" -> "playing" -> "name_input" -> "game_over" -> (R) "playing" ...
state = "menu"
top_scores = load_top_scores()  # Challenge 12: best scores read from scores.txt at startup


def reset_game():
    """Challenge 5: put everything back to its initial state (the high score is kept)"""
    global player, player2, obstacles, powerups, score, game_time
    global last_obstacle_spawn_time, last_powerup_spawn_time
    global paused, player_name, save_error

    player = Player(375, 530)
    player2 = Player(100, 100, PLAYER_COLOR2, PLAYER_SPEED)
    obstacles = []   # List to store obstacles
    powerups = []    # Challenge 11: list to store power-ups
    score = 0        # The score goes back to zero

    # Challenge 4 and 6: our own game clock (in milliseconds). It only advances while the
    # game is really running, so it does not count the time spent in pause or in Game Over.
    game_time = 0
    last_obstacle_spawn_time = 0
    last_powerup_spawn_time = 0

    paused = False
    player_name = ""
    save_error = False


def draw_text(text, text_font, color, x, y, align="left"):
    """Helper to draw text aligned to the left, center or right of x"""
    image = text_font.render(text, True, color)
    rect = image.get_rect()
    if align == "center":
        rect.midtop = (x, y)
    elif align == "right":
        rect.topright = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def finish_name_input():
    """Challenge 12: save the score with the typed name and show the Game Over screen"""
    global state, top_scores, save_error
    name = player_name.strip() or "PLAYER"
    save_error = not save_score(name, score)
    top_scores = load_top_scores()
    state = "game_over"


def draw_top_scores(y):
    draw_text("Top 5", font, (255, 255, 0), WIDTH // 2, y, "center")
    if not top_scores:
        draw_text("No scores yet", small_font, TEXT_COLOR, WIDTH // 2, y + 35, "center")
    for i, (name, value) in enumerate(top_scores):
        draw_text(f"{i + 1}. {name}  -  {value}", small_font, TEXT_COLOR, WIDTH // 2, y + 35 + i * 28, "center")


reset_game()

# GAME LOOP
running = True
while running:
    dt = clock.tick(FPS)  # milliseconds since the previous frame

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    state = "playing"

            elif state == "playing":
                # Challenge 4: ESC pauses and resumes the game
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif not paused:
                    # Challenge 8: KEYDOWN happens once per press, so each press changes the speed once
                    if event.unicode == "+" or event.key == pygame.K_KP_PLUS:
                        player.change_speed(1)
                    elif event.unicode == "-" or event.key == pygame.K_KP_MINUS:
                        player.change_speed(-1)

            elif state == "name_input":
                # Challenge 12: text entry made with Pygame events
                if event.key == pygame.K_RETURN:
                    finish_name_input()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode and event.unicode.isprintable() and event.unicode != ";" \
                        and len(player_name) < MAX_NAME_LENGTH:
                    player_name += event.unicode

            elif state == "game_over":
                # Challenge 5: R starts a new game without closing the program
                if event.key == pygame.K_r:
                    reset_game()
                    state = "playing"

    # ---------------- UPDATE ----------------
    if state == "playing" and not paused:
        game_time += dt

        # Challenge 7: every 10 points the delay is 50 ms shorter, never below 150 ms
        spawn_delay = max(MIN_SPAWN_DELAY, SPAWN_OBSTACLE_DELAY - SPAWN_DELAY_STEP * (score // POINTS_PER_LEVEL))

        # OBSTACLES spawning logic
        if game_time - last_obstacle_spawn_time > spawn_delay:
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = game_time

        # Challenge 11: a power-up appears every few seconds
        if game_time - last_powerup_spawn_time > POWERUP_SPAWN_DELAY:
            powerups.append(PowerUp())
            last_powerup_spawn_time = game_time

        # Update the position of each obstacle
        remaining_obstacles = []
        for obstacle in obstacles:
            obstacle.move()

            # Challenge 3 + 10: both players can be hit. A hit costs one life (not the whole game)
            hit = False
            for p in (player, player2):
                if p.is_alive() and not p.is_invulnerable(game_time) and p.rect.colliderect(obstacle.rect):
                    p.take_hit(game_time)
                    hit = True
            if hit:
                continue  # the obstacle that hit a player disappears

            # Remove obstacles that are off the screen
            if obstacle.is_off_screen():
                score += 1  # Increment the score for each obstacle that goes off screen
            else:
                remaining_obstacles.append(obstacle)
        obstacles = remaining_obstacles

        # Challenge 11: move power-ups and let the players collect them
        remaining_powerups = []
        for powerup in powerups:
            powerup.move()
            collected = False
            for p in (player, player2):
                if p.is_alive() and p.rect.colliderect(powerup.rect):
                    powerup.apply(p, game_time)
                    collected = True
                    break
            if not collected and not powerup.is_off_screen():
                remaining_powerups.append(powerup)
        powerups = remaining_powerups

        # Update the players' position (a player without lives does not move)
        if player.is_alive():
            player.moveArrows()
        if player2.is_alive():
            player2.moveWASD()
        player.update_effects(game_time)
        player2.update_effects(game_time)

        # Challenge 9: keep the best score of this execution
        high_score = max(high_score, score)

        # Challenge 10: the game ends when both players have no lives left
        if not player.is_alive() and not player2.is_alive():
            state = "name_input"
            player_name = ""

    # ---------------- DRAW ----------------
    screen.fill(BACKGROUND_COLOR)

    if state == "menu":
        draw_text("DODGE THE OBSTACLES", big_font, TEXT_COLOR, WIDTH // 2, 60, "center")
        draw_text("Player 1: arrow keys  (+ / - change speed)", small_font, PLAYER_COLOR, WIDTH // 2, 150, "center")
        draw_text("Player 2: W A S D", small_font, PLAYER_COLOR2, WIDTH // 2, 185, "center")
        draw_text("ESC: pause", small_font, TEXT_COLOR, WIDTH // 2, 220, "center")
        draw_top_scores(280)
        draw_text("Press ENTER to start", font, (0, 255, 0), WIDTH // 2, 500, "center")

    else:
        player.draw(screen, game_time)   # Draw the player rectangle (only if it has lives)
        player2.draw(screen, game_time)  # Draw the second player rectangle
        for obstacle in obstacles:
            obstacle.draw(screen)  # Draw each obstacle
        for powerup in powerups:
            powerup.draw(screen)

        # Display the score, the high score and the survival time (Challenges 6 and 9)
        draw_text(f"Score: {score}", font, TEXT_COLOR, 10, 10)
        draw_text(f"High score: {high_score}", font, (255, 255, 0), 10, 40)
        draw_text(f"Time: {game_time // 1000} s", font, TEXT_COLOR, 10, 70)

        # Lives and speed of each player (Challenges 8 and 10)
        draw_text(f"P1  Lives: {player.lives}  Speed: {player.current_speed()}", small_font, PLAYER_COLOR,
                  WIDTH - 10, 10, "right")
        draw_text(f"P2  Lives: {player2.lives}", small_font, PLAYER_COLOR2, WIDTH - 10, 40, "right")

        if paused:
            draw_text("PAUSE", big_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 40, "center")

        if state == "name_input":
            draw_text("Game Over", big_font, (255, 0, 0), WIDTH // 2, 150, "center")
            draw_text(f"Score: {score}", font, TEXT_COLOR, WIDTH // 2, 230, "center")
            draw_text("Enter your name and press ENTER:", font, TEXT_COLOR, WIDTH // 2, 290, "center")
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            draw_text(player_name + cursor, big_font, (255, 255, 0), WIDTH // 2, 330, "center")

        elif state == "game_over":
            draw_text("Game Over", big_font, (255, 0, 0), WIDTH // 2, 80, "center")
            draw_text(f"Score: {score}", font, TEXT_COLOR, WIDTH // 2, 160, "center")
            draw_top_scores(220)
            if save_error:
                draw_text("Could not save scores.txt", small_font, (255, 100, 100), WIDTH // 2, 420, "center")
            draw_text("Press R to restart", font, (0, 255, 0), WIDTH // 2, 480, "center")

    pygame.display.flip()

# Quit Pygame
pygame.quit()
