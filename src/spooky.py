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
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.astar_direction
        self.pacman = pacman
        self.mode = ContollerOfModes(self)
        self.blinky = blinky
        self.home_node = node

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

    def spawn(self):
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node):
        self.spawn_node = node

    def start_spawn(self):
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.direction_method = self.astar_direction
            self.spawn()

class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED

class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK

    def scatter(self):
        self.goal = Vector2(TITLEWIDTH * NCOLS, 0)

    def chase(self):
        pacman_direction = self.pacman.direction
        pacman_position = self.pacman.position
        target_position = pacman_position + self.pacman.directions[pacman_direction] * TITLEWIDTH * 4
        self.goal = target_position

class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.blinky = blinky

    def scatter(self):
        self.goal = Vector2(TITLEWIDTH * NCOLS, TITLEHEIGHT * NROWS)

    def chase(self):
        pacman_direction = self.pacman.direction
        pacman_position = self.pacman.position
        blinky_position = self.blinky.position

        # Calculate the position 2 tiles in front of Pac-Man
        vec1 = pacman_position + self.pacman.directions[pacman_direction] * TITLEWIDTH * 2

        # Calculate the vector from Blinky to the position 2 tiles in front of Pac-Man
        vec2 = (vec1 - blinky_position) * 2

        # Set Inky's goal to the position obtained by adding vec2 to Blinky's position
        self.goal = blinky_position + vec2

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE

    def scatter(self):
        self.goal = Vector2(0, TITLEHEIGHT * NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        d_square = d.magnitude_squared()
        if d_square <= (TITLEWIDTH * 8) ** 2:
            self.scatter()
        else:
            pacman_direction = self.pacman.direction
            pacman_position = self.pacman.position
            self.goal = pacman_position + self.pacman.directions[pacman_direction] * TITLEWIDTH * 4


class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [
            self.blinky,
            self.pinky,
            self.inky,
            self.clyde
        ]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def start_freight(self):
        for ghost in self:
            ghost.start_freight()
        self.reset_points()

    def set_spawn_node(self, node):
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self):
        for ghost in self:
            ghost.points *= 2

    def reset_points(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
