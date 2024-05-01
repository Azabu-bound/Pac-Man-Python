import pygame
from vector import Vector2
from const import *

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {
            UP:None,
            DOWN:None,
            LEFT:None,
            RIGHT:None
        }

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.as_tuple()
                line_end = self.neighbors[n].position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)

class NodeGroup(object):
    def __init__(self):
        self.node_list = []

    def test_nodes(self):
        nodeA = Node(80, 80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)

        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeA
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF

        self.node_list = [
            nodeA,
            nodeB,
            nodeC,
            nodeD,
            nodeE,
            nodeF,
            nodeG
        ]

    def render(self, screen):
        for node in self.node_list:
            node.render(screen)
