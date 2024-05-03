"""
For things that go bump in the night...
"""
import pygame
from pygame.locals import *
from vector import Vector2
from const import *
from entity import Entity
from actions import ContollerOfModes
from pacman import Pacman

class Ghost(Entity):
    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.astar_direction
        self.pacman = pacman
        self.mode = ContollerOfModes(self)

    def update(self, dt) -> None:
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        print(f"Ghost mode: {self.mode.current}, Goal: {self.goal}, Direction method: {self.direction_method}")
        Entity.update(self, dt)

    def scatter(self) -> None:
        self.goal = Vector2()

    def chase(self) -> None:
        if self.pacman is not None:
            self.goal = self.pacman.position
            self.direction_method = self.astar_direction
            print(f"Chasing Pacman: {self.goal}")
        else:
            print("Pacman object is None")

    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def normal_mode(self):
        self.set_speed(100)
        self.direction_method = self.astar_direction
