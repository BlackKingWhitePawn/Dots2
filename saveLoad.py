import json
import os
from images import Images
from dot import Dot
from playerMan import PlayerMan
from playerBot import PlayerBot

img_dict = {
    Images.red: 'r',
    Images.blue: 'b',
    Images.green: 'g',
    Images.gray: '0',
    Images.yellow: 'y',
    Images.marine: 'm',
    Images.pink: 'p',
    Images.purple: 'u',
    Images.orange: 'o'
}


def save(game, name):
    game_state = {
        'matrix': format_matrix(game.info.game_matrix),
        'order': game.order,
        'players': format_players(game.players)
    }

    for file_name in os.listdir('saves'):
        if file_name == name:
            return 'The ' + name + ' is already exist'

    with open(name, 'w') as f:
        json.dump(game_state, f)


def format_matrix(game_matrix):
    gm = list()
    for x in range(len(game_matrix)):
        gm.append(list())
        for y in range(len(game_matrix[0])):
            dot = game_matrix[x][y]
            gm[x].append([dot.x, dot.y, img_dict[dot.image]])

    return gm


def enformat_matrix(format_game_matrix):
    img_dict2 = {v: k for k, v in img_dict.items()}
    gm = list()
    for x in range(len(format_game_matrix)):
        gm.append(list())
        for y in range(len(format_game_matrix[0])):
            elem = format_game_matrix[x][y]
            gm[x].append(Dot(elem[0], elem[1], img_dict2[elem[2]]))

    return gm


def format_players(players):
    return [(img_dict[x.color], x.is_man) for x in players]


def enformat_players(format_players2):
    img_dict2 = {v: k for k, v in img_dict.items()}
    return [(PlayerBot(img_dict2[x[0]]), PlayerMan(img_dict2[x[0]]))[x[1]] for x in format_players2]


def load(name):
    for file_name in os.listdir('saves'):
        if file_name == name:
            os.chdir('saves')
            with open(name) as f:
                game_state = json.load(f)
                game_state['matrix'] = enformat_matrix(game_state['matrix'])
                game_state['players'] = enformat_players(game_state['players'])
                os.chdir('..')
                return game_state
