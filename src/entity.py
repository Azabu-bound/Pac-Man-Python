import pygame
from pygame.locals import *
from nodes import Node
from vector import Vector2
from const import *
from random import randint
import heapq

class PriorityEntry:
    def __init__(self, priority, cost, node):
        self.priority = priority
        self.cost = cost
        self.node = node

    def __lt__(self, other):
        return (self.priority < other.priority) or (self.priority == other.priority and self.cost < other.cost)

    def __eq__(self, other):
        return self.node == other.node and self.cost == other.cost and self.priority == other.priority

class Entity(object):
    def __init__(self, node) -> None:
        self.name = None
        self.directions = {
            UP:Vector2(0, -1),
            DOWN:Vector2(0, 1),
            LEFT:Vector2(-1, 0),
            RIGHT:Vector2(1, 0),
            STOP:Vector2()
        }
        self.direction = STOP
        self.set_speed(100)
        self.radius = 10
        self.collide_radius = 5
        self.color = WHITE
        #self.node = node
        #self.set_position()
        #self.target = node
        self.visible = True
        self.disable_portal = False
        self.goal = None
        self.direction_method = self.random_direction
        self.set_start_node(node)

    def set_between_nodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) * 0.5

    def reset(self):
        self.set_start_node(self.start_node)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def set_start_node(self, node):
        self.node = node
        self.start_node = node
        self.target = node
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()

    def valid_direction(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None: return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2_target = vec1.magnitude_squared()
            node2_self = vec2.magnitude_squared()
            return node2_self >= node2_target
        return False

    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1: return True
        return False

    def set_speed(self, speed):
        self.speed = speed * TITLEWIDTH / 16

    def render(self, screen):
        if self.visible:
            p = self.position.as_int()
            pygame.draw.circle(screen, self.color, p, self.radius)

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshot_target():
            self.node = self.target
            directions = self.valid_directions()
            #direction = self.random_direction(directions)
            direction = self.direction_method(directions)
            if not self.disable_portal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions):
        return directions[randint(0, len(directions)-1)]
    """"
    Original pathfindng algorithm:

    def goal_direction(self, directions):
        distances = []
        for d in directions:
            vec = self.node.position  + self.directions[d]*TITLEWIDTH - self.goal
            distances.append(vec.magnitude_squared())
        i = distances.index(min(distances))
        return directions[i]
    """

    """
    A* algorithm implementation.
    LET'GO!
    I will import heapq.
    """
    def astar_direction(self, directions):
        queue = []
        cost = {self.node: 0}
        previous = {self.node: None}

        heapq.heappush(queue, PriorityEntry(0, 0, self.node))  # Push the starting node

        while queue:
            current_entry = heapq.heappop(queue)  # Pop the entry with the lowest priority
            current_cost = current_entry.cost
            current_node = current_entry.node

            if current_node.position == self.goal:
                path = []
                while current_node != self.node:
                    path.append(current_node)
                    current_node = previous[current_node]
                path.append(self.node)
                path.reverse()
                if len(path) > 1:
                    next_node = path[1]
                    for d in directions:
                        if self.node.neighbors[d] == next_node:
                            return d
                break

            for d in directions:
                neighbor = self.node.neighbors[d]
                if neighbor is not None:
                    new_cost = current_cost + 1
                    if neighbor not in cost or new_cost < cost[neighbor]:
                        cost[neighbor] = new_cost
                        priority = new_cost + self.heuristic(neighbor.position, self.goal)
                        heapq.heappush(queue, PriorityEntry(priority, new_cost, neighbor))
                        previous[neighbor] = current_node

            if not queue:
                    # If no path is found, return the direction that brings the ghost closer to the goal
                    min_distance = float('inf')
                    closest_direction = None
                    for d in directions:
                        neighbor = self.node.neighbors[d]
                        if neighbor is not None:
                            distance = self.heuristic(neighbor.position, self.goal)
                            if distance < min_distance:
                                min_distance = distance
                                closest_direction = d
                    if closest_direction is not None:
                        return closest_direction

        return self.random_direction(directions)

    def heuristic(self, a, b):
        # Manhattan distance heuristic
        return abs(a.x - b.x) + abs(a.y - b.y)
