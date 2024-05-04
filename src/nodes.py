import pygame
from vector import Vector2
from const import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {
            UP:None,
            DOWN:None,
            LEFT:None,
            RIGHT:None,
            PORTAL:None
        }
        self.access = {
            UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE],
            DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE],
            LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE],
            RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE,]
        }

    def thou_shall_not_pass(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def move_along(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    #def __it__(self, other):
    #    return self.position.x < other.position.x or (self.position.x == other.position.x and self.position.y < other.position.y)

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.as_tuple()
                line_end = self.neighbors[n].position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, GRAY, self.position.as_int(), 12)

class NodeGroup(object):
    def __init__(self, level):
        #self.node_list = []
        self.level = level
        self.nodes_LUT = {}
        self.node_symbols = ['+', 'P', 'n']
        self.path_symbols = ['.', '-', '|', 'p']
        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)
        self.homekey = None

    # Read the text file
    def read_maze_file(self, textfile):
        return np.loadtxt(textfile, dtype = '<U1') # set dtype to U1 to avoid errors when encountering '.'

    # Generate node table
    def create_node_table(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col+xoffset, row+yoffset)
                    self.nodes_LUT[(x, y)] = Node(x, y)

    def construct_key(self, x, y):
      return x * TITLEWIDTH, y * TITLEHEIGHT

    def connect_horizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col+xoffset, row+yoffset)
                    else:
                        other_key = self.construct_key(col+xoffset, row+yoffset)
                        self.nodes_LUT[key].neighbors[RIGHT] = self.nodes_LUT[other_key]
                        self.nodes_LUT[other_key].neighbors[LEFT] = self.nodes_LUT[key]
                        key = other_key
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_vertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col] [row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col+xoffset, row+yoffset)
                    else:
                        other_key = self.construct_key(col+xoffset, row+yoffset)
                        self.nodes_LUT[key].neighbors[DOWN] = self.nodes_LUT[other_key]
                        self.nodes_LUT[other_key].neighbors[UP] = self.nodes_LUT[key]
                        key = other_key
                elif dataT[col] [row] not in self.path_symbols:
                    key = None

    def get_node_from_pixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodes_LUT.keys():
            return self.nodes_LUT[(xpixel, ypixel)]
        return None

    def get_node_from_tiles(self, col, row):
        x, y = self.construct_key(col, row)
        if (x, y) in self.nodes_LUT.keys():
            return self.nodes_LUT[(x, y)]
        return None

    def get_start_temp_node(self):
        nodes = list(self.nodes_LUT.values())
        return nodes[0]

    def render(self, screen):
        for node in self.nodes_LUT.values():
            node.render(screen)

    def set_portal_pair(self, pair1, pair2):
        key1 = self.construct_key(*pair1)
        key2 = self.construct_key(*pair2)
        if key1 in self.nodes_LUT.keys() and key2 in self.nodes_LUT.keys():
            self.nodes_LUT[key1].neighbors[PORTAL] = self.nodes_LUT[key2]
            self.nodes_LUT[key2].neighbors[PORTAL] = self.nodes_LUT[key1]

    def create_home_nodes(self, xoffset, yoffset):
        homedata = np.array([
            ['X','X','+','X','X'],
            ['X','X','.','X','X'],
            ['+','X','.','X','+'],
            ['+','.','+','.','+'],
            ['+','X','X','X','+']
        ])

        self.create_node_table(homedata, xoffset, yoffset)
        self.connect_horizontally(homedata, xoffset, yoffset)
        self.connect_vertically(homedata, xoffset, yoffset)
        self.homekey = self.construct_key(xoffset + 2, yoffset)
        return self.homekey

    def connect_home_nodes(self, homekey, otherkey, direction):
        key = self.construct_key(*otherkey)
        self.nodes_LUT[homekey].neighbors[direction] = self.nodes_LUT[key]
        self.nodes_LUT[key].neighbors[direction * -1] = self.nodes_LUT[homekey]

    def thou_shall_not_pass(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node is not None:
            node.thou_shall_not_pass(direction, entity)

    def move_along(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node is not None:
            node.move_along(direction, entity)

    def thou_shall_not_pass_list(self, col, row, direction, entities):
        for e in entities:
            self.thou_shall_not_pass(col, row, direction, e)

    def move_along_list(self, col, row, direction, entities):
        for e in entities:
            self.move_along(col, row, direction, e)

    def deny_home_access(self, entity):
        self.nodes_LUT[self.homekey].thou_shall_not_pass(DOWN, entity)

    def allow_home_access(self, entity):
        self.nodes_LUT[self.homekey].move_along(DOWN, entity)

    def deny_home_access_list(self, entities):
        for e in entities:
            self.deny_home_access(e)

    def allow_home_access_list(self, entities):
        for e in entities:
            self.allow_home_access(e)
