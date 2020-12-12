from player.player import Player
from random import randint


class PlayerBot(Player):

    def __init__(self, color, name="default", ai_level=0):
        self.color = color
        self.name = name
        self.points = 0
        self.is_man = False
        self.level = ai_level

    def make_move(self, game_matrix):
        if self.level == 0:
            return randint(0, len(game_matrix) - 1), randint(0, len(game_matrix[0]) - 1)

    def get_chain(self, dot_coords):
        chain = []
        used = set()
        self.recurrence_find_chain(dot_coords, chain, used, dot_coords)
        return chain

    def get_neighbours(self, dot_coords):
        nb_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= dot_coords[0] + i < self.field[0] and 0 <= dot_coords[1] + j < self.field[1] and not (
                        i == 0 and j == 0):
                    nb_list.append((dot_coords[0] + i, dot_coords[1] + j))

        if nb_list is None:
            return None
        return set(nb_list)

    def recurrence_find_chain(self, start, chain, used, elem):
        chain.append(elem)
        used.add(elem)
        nb_list = self.get_neighbours(elem)
        for e in nb_list:
            if e == start:
                return
            if e in used:
                continue
            if self.game_matrix[e[0]][e[1]].color == self.game_matrix[start[0]][start[1]].color:
                return self.recurrence_find_chain(start, chain, used, e)

        chain.clear()

    def large_find_chain(self, start, used, queue):
        pass


class Node:

    def __init__(self, dot, previous=None):
        self.dot = dot  # tuple - dot coordinates
        self.previous = previous  # Node - previous node


class Chain:

    def __init__(self, path=None):
        self.start = Node(path[0])  # Node - first node in path
        self.path = path  # List of tuple - path
        last = None
        current = None
        for dot in path:
            current = Node(dot, last)
            last = current

        self.end = current  # Node - last node in path
        self.count = len(path)  # int - path length

    def append(self, dot):
        self.end = Node(dot, self.end)
        self.path.append(dot)
