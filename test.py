from game import Game as t
from dot import Dot

GAME = t((3, 3))
GAME.game_matrix = [
    [Dot(0, 0), Dot(0, 1), Dot(0, 2)],
    [Dot(0, 1), Dot(0, 1), Dot(0, 1)],
    [Dot(0, 1), Dot(0, 1), Dot(0, 1)]
]
GAME.game_matrix[0][1].change_color('Red')
GAME.game_matrix[1][0].change_color('Red')
GAME.game_matrix[1][2].change_color('Red')
GAME.game_matrix[2][1].change_color('Red')


def get_chain(game, dot):
    chain = []
    used = []
    recurrence_find_chain(game, dot, chain, used, dot)
    return chain


def get_neighbours(game, dot_coords):
    nb_list = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= dot_coords[0] + i < game.field[0] and 0 <= dot_coords[1] + j < game.field[1] and not (i == 0 and j == 0):
                nb_list.append((dot_coords[0] + i, dot_coords[1] + j))

    return nb_list


def recurrence_find_chain(game, start, chain, used, elem):
    chain.append(elem)
    used.append(elem)
    nb_list = get_neighbours(game, elem)
    for e in nb_list:
        if e == start:
            return
        if e in used:
            continue
        if game.game_matrix[e[0]][e[1]].get_color() == game.game_matrix[start[0]][start[1]].get_color():
            return recurrence_find_chain(game, chain, start, used, e)

    chain.clear()


#print(get_chain(GAME, (1, 0)))
print(get_neighbours(GAME, (0, 1)))
