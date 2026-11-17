# Moving Player Game - Pygame

Two-player arcade game made with Pygame. Obstacles fall from the top of the window and the players have to dodge them. Every obstacle that leaves the screen gives one point.

## Gameplay video

<video src="gameplay.mp4" controls width="640"></video>

[Watch the gameplay video](gameplay.mp4)

## How to play

1. Install Pygame: `pip install pygame`
2. Run the game: `python main.py`

| Key | Action |
|---|---|
| Arrow keys | Move player 1 (blue) |
| `W` `A` `S` `D` | Move player 2 (orange) |
| `+` / `-` | Increase / decrease the speed of player 1 (2 to 12) |
| `ESC` | Pause / resume |
| `ENTER` | Start the game (menu) / save your name (after Game Over) |
| `R` | Restart after Game Over |

## Project structure

| File | Content |
|---|---|
| `main.py` | Game loop, game states, scoring, pause, restart, HUD |
| `player.py` | `Player` class: movement, boundaries, speed, lives, effects |
| `obstacle.py` | `Obstacle` class |
| `powerup.py` | `PowerUp` class (Challenge 11) |
| `scores.py` | Reading and writing `scores.txt` (Challenge 12) |
| `config.py` | All the constants (sizes, speeds, delays, durations) |

## Part 1 - Mandatory challenges

### 1. Player boundaries
`Player.keep_inside()` calls `self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))`, which moves the rectangle back inside the window if any side goes out. It is called at the end of `moveArrows()` and `moveWASD()`, so it works for both players and for the four sides (left, right, top, bottom).

### 2. Random obstacle sizes
In `Obstacle.__init__` the size is `random.randint(OBSTACLE_SIZE_MIN, OBSTACLE_SIZE_MAX)` (20 to 70). The `x` position is chosen between `0` and `WIDTH - size`, so the obstacle always appears completely inside the width of the window.

### 3. Collision with Player 2
In the obstacle loop of `main.py` the collision is checked for both players with `for p in (player, player2)` and `p.rect.colliderect(obstacle.rect)`. (Together with Challenge 10, a hit now costs a life, and the game ends when both players run out of lives.)

### 4. Pause game
Pressing `ESC` in the `"playing"` state toggles the `paused` variable. The whole update block is inside `if state == "playing" and not paused:`, so while paused nobody moves, obstacles do not fall and no new obstacles appear. The message `PAUSE` is drawn on the screen.

### 5. Restart game
In the `"game_over"` state, pressing `R` calls `reset_game()`. This function creates new players in their initial positions, empties the obstacle and power-up lists, sets the score and the timers to zero and restores the lives. The high score is stored outside of that function, so it is kept.

### 6. Survival timer
The game has its own clock, `game_time` (in milliseconds), that is increased with `dt = clock.tick(FPS)` only while the game is running. Because of that, it stops in Game Over and it does not advance during a pause (using `pygame.time.get_ticks()` directly would keep counting while paused). The HUD shows `game_time // 1000` as seconds.

### 7. Increasing difficulty
The delay between obstacles is calculated every frame as
`max(MIN_SPAWN_DELAY, SPAWN_OBSTACLE_DELAY - SPAWN_DELAY_STEP * (score // POINTS_PER_LEVEL))`.
Every 10 points the delay is 50 ms shorter (500, 450, 400...) and it never goes below 150 ms. Since it is calculated from the score, it goes back to 500 ms automatically when the game restarts.

### 8. Change player speed
In the `KEYDOWN` event, `+` and `-` call `player.change_speed(1)` / `change_speed(-1)`. `KEYDOWN` is triggered once per key press, so each press changes the speed only once. `change_speed` uses `max(2, min(12, ...))` to keep the speed between 2 and 12. Only player 1 can change it, and the current speed is shown in the HUD.

### 9. High score
The variable `high_score` is created once, before the game loop, and updated with `max(high_score, score)`. `reset_game()` does not touch it, so it is kept between games. It is displayed below the current score.

## Part 2 - Additional challenges

### 10. Lives system
Each `Player` starts with 3 lives. `take_hit()` removes one life and sets `hit_until = now + 2000`; while `now < hit_until` the player is invulnerable (it blinks) and cannot lose more lives from the same collision. The obstacle that hit the player disappears. A player with 0 lives is not drawn and cannot move. The state changes to Game Over only when both players have no lives left.

### 11. Power-ups
The class `PowerUp` is in its own file, `powerup.py`. A new one appears every 8 seconds (`POWERUP_SPAWN_DELAY`) and falls down. When a living player touches it, `apply(player, now)` gives the effect:
- **Yellow `S` (speed):** +4 speed for 5 seconds.
- **Green `+` (life):** recovers one life (maximum 5).
- **Cyan `I` (shield):** invulnerable for 5 seconds (white frame around the player).

Temporary effects are stored as an end time (`speed_boost_until`, `shield_until`). `Player.update_effects()` removes the speed bonus automatically when the time is over, and `is_invulnerable()` stops being true by itself when the shield time ends.

### 12. Save high scores in a file
When the game ends the player types a name using Pygame events (`KEYDOWN`, with `event.unicode`, `BACKSPACE` to delete and `ENTER` to confirm). `save_score(name, score)` in `scores.py` appends a line `name;score` to `scores.txt`. `load_top_scores()` reads the file, sorts the scores from highest to lowest and returns the best five. They are shown on the start menu and on the Game Over screen. If the file cannot be written, the game shows a message instead of crashing.
