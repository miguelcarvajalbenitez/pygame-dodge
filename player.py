
import pygame
from config import *

class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        """Initialize the player with a position and size"""
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = speed
        # Challenge 10: lives and invulnerability after a hit
        self.lives = PLAYER_LIVES
        self.hit_until = 0           # game time (ms) until the post-hit invulnerability ends
        # Challenge 11: temporary effects from power-ups
        self.shield_until = 0        # invulnerable until this game time (ms)
        self.speed_bonus = 0         # extra speed while the speed boost is active
        self.speed_boost_until = 0

    def current_speed(self):
        """Speed used for movement (base speed + power-up bonus)"""
        return self.speed + self.speed_bonus

    def keep_inside(self):
        """Challenge 1: stop the player from leaving the window on any of the four sides"""
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def moveArrows(self):
        """Update the player's position based on keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        speed = self.current_speed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_UP]:
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:
            self.rect.y += speed
        self.keep_inside()

    def moveWASD(self):
        """Update the player's position based on WASD keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        speed = self.current_speed()

        if keys[pygame.K_a]:
            self.rect.x -= speed
        if keys[pygame.K_d]:
            self.rect.x += speed
        if keys[pygame.K_w]:
            self.rect.y -= speed
        if keys[pygame.K_s]:
            self.rect.y += speed
        self.keep_inside()

    def change_speed(self, amount):
        """Challenge 8: change the base speed, always between the minimum and the maximum"""
        self.speed = max(PLAYER_SPEED_MIN, min(PLAYER_SPEED_MAX, self.speed + amount))

    def is_alive(self):
        """Challenge 10: a player is alive while it has lives left"""
        return self.lives > 0

    def is_invulnerable(self, now):
        """Challenge 10 / 11: True after a hit or while the shield power-up is active"""
        return now < max(self.hit_until, self.shield_until)

    def take_hit(self, now):
        """Challenge 10: lose one life and get 2 seconds of invulnerability"""
        self.lives -= 1
        self.hit_until = now + INVULNERABLE_TIME

    def update_effects(self, now):
        """Challenge 11: remove temporary effects automatically when their time is over"""
        if now >= self.speed_boost_until:
            self.speed_bonus = 0

    def draw(self, surface, now=0):
        """Draw the player on the given surface (nothing is drawn if it has no lives left)"""
        if not self.is_alive():
            return
        # Blink while invulnerable after a hit
        blinking = now < self.hit_until and (now // 100) % 2 == 0
        if not blinking:
            pygame.draw.rect(surface, self.color, self.rect)
        # White frame while the shield is active
        if now < self.shield_until:
            pygame.draw.rect(surface, TEXT_COLOR, self.rect.inflate(10, 10), 3)
