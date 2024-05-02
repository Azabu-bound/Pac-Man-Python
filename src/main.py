import pygame
from pygame.locals import *
from const import *
from pacman import Pacman
from nodes import NodeGroup

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
        self.nodes = NodeGroup("mazetest.txt")
        self.pacman = Pacman(self.nodes.get_start_temp_node())

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.check_events()
        self.render()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT: exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pacman.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
