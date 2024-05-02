import pygame
from vector import Vector2
from const import *
import numpy as np

class Pellet(object):
    def __init__(self, row, col):
        self.name = PELLET
        self.position = Vector2(col * TITLEWIDTH, row * TITLEHEIGHT)
        self.color = WHITE
        self.radius = int(4 * TITLEWIDTH / 16)
        self.collide_radius = int(4 * TITLEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.position.as_int()
            pygame.draw.circle(screen, self.color, p, self.radius)

class PowerUpPellet(Pellet):
    def __init__(self, row, col):
        Pellet.__init__(self, row, col)
        self.name = POWERUPPELLET
        self.radius = int(8 * TITLEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0

class Pellets_Group(object):
    def __init__(self, pelletfile):
        self.pellet_list = []
        self.powerup_pellets = []
        self.form_pellet_list(pelletfile)
        self.number_eaten = 0

    def update(self, dt):
        for power_up_pellet in self.powerup_pellets:
            power_up_pellet.update(dt)

    def form_pellet_list(self, pelletfile):
        data = self.read_pell_file(pelletfile)

        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row] [col] in ['.', '+']:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row] [col] in ['P', 'p']:
                    p_p = PowerUpPellet(row, col)
                    self.pellet_list.append(p_p)
                    self.powerup_pellets.append(p_p)

    def read_pell_file(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def is_empty(self):
        if len(self.pellet_list) == 0: return True
        return False

    def render(self, screen):
        for p in self.pellet_list:
            p.render(screen)
