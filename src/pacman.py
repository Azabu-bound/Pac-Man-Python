import pygame
from pygame.locals import *
from vector import Vector2
from const import *

class Pacman(object):
    def __init__(self):
        self.name = PACMAN
        self.position = Vector2(200, 400)
        self.directions = {
            STOP:Vector2(),
            UP:Vector2(0, -1),
            DOWN:Vector2(0, 1),
            LEFT:Vector2(-1, 0),
            RIGHT:Vector2(1, 0)
        }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.radius = 10
        self.color = YELLOW

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()
        self.direction = direction

    def get_valid_key(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]: return UP
        if key_pressed[K_DOWN]: return DOWN
        if key_pressed[K_LEFT]: return LEFT
        if key_pressed[K_RIGHT]: return RIGHT
        return STOP

    def render(self, screen):
        p = self.position.as_int()
        pygame.draw.circle(screen, self.color, p, self.radius)
