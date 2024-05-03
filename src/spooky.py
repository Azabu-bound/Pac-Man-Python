"""
For things that go bump in the night...
"""
import pygame
from pygame.locals import *
from vector import Vector2
from const import *
from entity import Entity

class Ghost(Entity):
    def __init__(self, node) -> None:
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.goal_direction
