import pygame
import random

from config import *


class PowerUp:
    """Challenge 11: special object that falls from the top and players can collect.

    Types:
      - "speed":  the player moves faster for a few seconds (yellow)
      - "life":   the player recovers one life (green)
      - "shield": the player is invulnerable for a few seconds (cyan)
    """

    COLORS = {"speed": (255, 255, 0), "life": (0, 255, 0), "shield": (0, 255, 255)}
    LETTERS = {"speed": "S", "life": "+", "shield": "I"}
    font = None  # created the first time a power-up is drawn

    def __init__(self):
        self.kind = random.choice(list(self.COLORS))
        x = random.randint(0, WIDTH - POWERUP_SIZE)
        self.rect = pygame.Rect(x, -POWERUP_SIZE, POWERUP_SIZE, POWERUP_SIZE)

    def move(self):
        self.rect.y += POWERUP_FALL_SPEED

    def is_off_screen(self):
        return self.rect.y > HEIGHT

    def apply(self, player, now):
        """Give the effect to the player. 'now' is the current game time in ms."""
        if self.kind == "speed":
            player.speed_bonus = POWERUP_SPEED_BONUS
            player.speed_boost_until = now + POWERUP_DURATION
        elif self.kind == "life":
            player.lives = min(MAX_LIVES, player.lives + 1)
        elif self.kind == "shield":
            player.shield_until = now + POWERUP_DURATION

    def draw(self, surface):
        pygame.draw.rect(surface, self.COLORS[self.kind], self.rect, border_radius=8)
        if PowerUp.font is None:
            PowerUp.font = pygame.font.Font(None, 26)
        letter = PowerUp.font.render(self.LETTERS[self.kind], True, (0, 0, 0))
        surface.blit(letter, letter.get_rect(center=self.rect.center))
