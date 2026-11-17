import os

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background
TEXT_COLOR = (255, 255, 255)
PLAYER_COLOR = (60, 140, 255)  # Blue player
PLAYER_COLOR2 = (255, 140, 60)  # Orange player
PLAYER_SPEED = 6  # Speed of the player movement

OBSTACLES_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

SPAWN_OBSTACLE_DELAY = 500  # milliseconds

# Challenge 2: random obstacle size
OBSTACLE_SIZE_MIN = 20
OBSTACLE_SIZE_MAX = 70

# Challenge 7: increasing difficulty
POINTS_PER_LEVEL = 10        # every 10 points...
SPAWN_DELAY_STEP = 50        # ...the spawn delay is reduced by 50 ms
MIN_SPAWN_DELAY = 150        # ...but never below 150 ms

# Challenge 8: player speed limits
PLAYER_SPEED_MIN = 2
PLAYER_SPEED_MAX = 12

# Challenge 10: lives
PLAYER_LIVES = 3
MAX_LIVES = 5
INVULNERABLE_TIME = 2000     # milliseconds after being hit

# Challenge 11: power-ups
POWERUP_SPAWN_DELAY = 8000   # milliseconds
POWERUP_DURATION = 5000      # milliseconds (speed boost and shield)
POWERUP_SPEED_BONUS = 4
POWERUP_SIZE = 30
POWERUP_FALL_SPEED = 3

# Challenge 12: scores file (saved next to the code)
SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.txt")
TOP_SCORES_COUNT = 5
MAX_NAME_LENGTH = 10
