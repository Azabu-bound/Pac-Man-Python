"""
For things that go bump in the night...
"""
import pygame
from pygame.locals import *
from vector import Vector2
from const import *
from entity import Entity
from actions import ContollerOfModes

class Ghost(Entity):
    def __init__(self, node, pacman=None) -> None:
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ContollerOfModes(self)

    def update(self, dt) -> None:
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self) -> None:
        self.goal = Vector2()

    def chase(self) -> None:
        self.goal = self.pacman.position
