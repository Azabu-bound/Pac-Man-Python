import pygame
from pygame.locals import *
from const import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import Pellets_Group
from spooky import GhostGroup
from pause import Pause

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        #self.lives = 3

    #def restart_game(self):
        #self.lives = 3
        #self.start_game()

    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self):
        self.set_background()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        homekey = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(homekey, (12, 14), LEFT)
        self.nodes.connect_home_nodes(homekey, (15, 14), RIGHT)
        #self.pacman = Pacman(self.nodes.get_start_temp_node())
        self.pacman = Pacman(self.nodes.get_node_from_tiles(15, 26))
        self.pellets = Pellets_Group("maze1.txt")
        #self.ghost = Ghost(self.nodes.get_start_temp_node(), self.pacman)
        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)
        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_tiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_tiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_tiles(4 + 11.5, 3 + 14))
        #self.ghost.set_spawn_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            #self.ghost.update(dt)
            self.ghosts.update(dt)
            self.pellet_events()
            self.check_ghost_events()
        post_pause_method = self.pause.update(dt)
        if post_pause_method is not None:
            post_pause_method()
        self.check_events()
        self.render()

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.set_pause(pause_time=1, func=self.show_sprites)
                    ghost.start_spawn()

    def show_sprites(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hide_sprites(self):
        self.pacman.visible = False
        self.ghosts.hide()
        #if self.pacman.collide_ghost(self.ghost):
            #if self.ghost.mode.current is FREIGHT:
                #self.ghost.start_spawn()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause.set_pause(player_paused=True)
                    if not self.pause.paused:
                        self.show_sprites()
                    else:
                        self.hide_sprites()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        #self.ghost.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()

    def pellet_events(self):
        p = self.pacman.consume_pellets(self.pellets.pellet_list)
        if p:
            self.pellets.number_eaten += 1
            self.pellets.pellet_list.remove(p)
            if p.name is POWERUPPELLET:
                #self.ghost.start_freight()
                self.ghosts.start_freight()
            if self.pellets.is_empty():
                print("You win! Congrats, and thanks for playing :)")
                pygame.quit()
                exit()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
