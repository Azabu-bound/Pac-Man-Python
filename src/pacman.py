import pygame
from pygame.locals import *
from nodes import Node
from vector import Vector2
from const import *
from entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()
        #self.direction = direction
        #self.node = self.get_new_target(direction)
        #self.set_position()
        if self.overshot_target():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
                #else:
                #self.direction = STOP
                #self.set_position()
            else:
                self.target = self.get_new_target(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()


    def get_valid_key(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]: return UP
        if key_pressed[K_DOWN] or key_pressed[K_s]: return DOWN
        if key_pressed[K_LEFT] or key_pressed[K_a]: return LEFT
        if key_pressed[K_RIGHT] or key_pressed[K_d]: return RIGHT
        return STOP

    def consume_pellets(self, pellet_list):
        for p in pellet_list:
            if self.collide_check(p):
                return p
            #d = self.position - p.position
            #d_square = d.magnitude_squared()
            #r_square = (p.radius + self.collide_radius) ** 2

            #if d_square <= r_square: return p
        return None

    def collide_ghost(self, ghost):
        return self.collide_check(ghost)

    def collide_check(self, other):
        d = self.position - other.position
        d_square = d.magnitude_squared()
        r_square = (self.collide_radius + other.collide_radius) ** 2

        if d_square <= r_square: return True
        return False

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True

    def die(self):
        self.alive = False
        self.directon = STOP
