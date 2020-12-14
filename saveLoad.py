import json
import os
from images import Images
from dots.dot import Dot
from player.playerMan import PlayerMan
from player.playerBot import PlayerBot

img_dict = {
    Images.red: 'red',
    Images.blue: 'blue',
    Images.green: 'green',
    Images.gray: 'gray',
    Images.yellow: 'yellow',
    Images.marine: 'marine',
    Images.pink: 'pink',
    Images.purple: 'purple',
    Images.orange: 'orange'
}


def save(game, name):
    game_state = {
        'matrix': format_matrix(game.info.game_matrix),
        'order': game.order,
        'players': format_players_to_data(game.players),
        'time': game.time,
        'timers': game.timers
    }

    for file_name in os.listdir('saves'):
        if file_name[:-4] == name[6:-4]:
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
            gm[x].append(Dot(ix=elem[0], iy=elem[1], image=img_dict2[elem[2]], color=img_dict[img_dict2[elem[2]]]))

    return gm


def format_players_to_data(players):
    return [(img_dict[x.color[1]], x.is_man) for x in players]


def format_data_to_players(format_players):
    img_dict2 = {v: k for k, v in img_dict.items()}
    return [(PlayerBot((x[0], img_dict2[x[0]])), PlayerMan((x[0], img_dict2[x[0]])))[x[1]] for x in format_players]


def load(name):
    for file_name in os.listdir('saves'):
        if file_name == name:
            os.chdir('saves')
            with open(name) as f:
                game_state = json.load(f)
                game_state['matrix'] = enformat_matrix(game_state['matrix'])
                game_state['players'] = format_data_to_players(game_state['players'])
                os.chdir('..')
                return game_state
