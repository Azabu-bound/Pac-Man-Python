import pygame
from pygame.locals import *
from const import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import Pellets_Group
from spooky import GHOST, Ghost

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()

    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self):
        self.set_background()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.get_start_temp_node())
        self.pellets = Pellets_Group("maze1.txt")
        self.ghost = Ghost(self.nodes.get_start_temp_node())

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.pellet_events()
        self.check_events()
        self.render()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT: exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()

    def pellet_events(self):
        p = self.pacman.consume_pellets(self.pellets.pellet_list)
        if p:
            self.pellets.number_eaten += 1
            self.pellets.pellet_list.remove(p)


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
