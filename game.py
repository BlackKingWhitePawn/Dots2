import json
import os

import pygame
import time

from gameTools.referee import Referee
from player.playerMan import PlayerMan
from saveLoad import save
from gameTools.gameInfo import GameInfo
from player.playerBot import PlayerBot
from images import Images
from controls.button import Button
from dots.colors import Colors
from recordsWindow import RecordWindow


class Game:

    def __init__(self, res, data, game_state=None, player_men=None, player_bot=None):
        if game_state is not None:
            self.players = game_state['players']
            self.order = game_state['order']
            self.info = GameInfo((data["n_x"], data['n_y']), res, game_state['matrix'])
            if 'timers' in game_state:
                self.timers = game_state['timers']
                self.time = True
            else:
                self.time = False
        else:
            self.players = player_men + player_bot
            self.order = 0
            self.info = GameInfo((data["n_x"], data['n_y']), res)
            self.time = False
            if data['time']:
                self.timers = {p.name: 0 for p in self.players}
                self.time = True

        self.data = {"new_game": False}
        self.over = False
        self.counter = 0
        self.winner = None
        self.init_records()

        def over():
            self.over = True

        def restart():
            self.info.window.fill(Colors.gray)
            self.order = 0
            self.info.game_matrix = self.info.init_matrix(self.info.field)
            self.info.is_over = False
            if self.time:
                self.timers = {p.name: 0 for p in self.players}

        def records():
            rw = RecordWindow()
            rw.run()
            self.info.window = pygame.display.set_mode(self.info.res)

        def new_game():
            self.data["new_game"] = True
            over()

        def save_game():
            name = self.handle_events_enter_text('')
            result = save(self, 'saves/' + name + '.txt')
            while result is not None:
                pygame.display.set_caption(result)
                # time.sleep(1)
                name = self.handle_events_enter_text(name)
                result = save(self, 'saves/' + name + '.txt')
            pygame.display.set_caption(name + ' was saved')

        self.buttons = {
            'New Game': Button((10, 10), (20, 20), new_game, Images.home),
            'Restart': Button((40, 10), (20, 20), restart, Images.restart),
            'Record table': Button((70, 10), (20, 20), records, Images.record),
            'Save': Button((100, 10), (20, 20), save_game, Images.save)
        }

        self.colors = {
            'red': Colors.red,
            'blue': Colors.blue,
            'green': Colors.green,
            'yellow': Colors.yellow,
            'pink': Colors.pink,
            'purple': Colors.purple,
            'marine': Colors.marine,
            'orange': Colors.orange,
        }

        pygame.display.set_caption('Dots')
        pygame.init()

    '''main loop'''

    def run(self):
        self.draw()
        while not self.over:
            if type(self.players[self.order]) is PlayerBot and not self.info.is_over:
                # time.sleep(0.7)
                self.make_move()
                self.draw()
            else:
                start = time.perf_counter()
                self.handle_events()
                self.draw()
                if self.time:
                    move_time = time.perf_counter() - start
                    if not self.info.is_over and self.time:
                        self.timers[self.players[self.order].name] += move_time

            self.draw()

    def init_records(self):
        for player in self.players:
            if not os.path.exists('records/players/{0}.txt'.format(player.name)):
                with open('records/players/{0}.txt'.format(player.name), 'w') as f:
                    empty_stats = {
                        "Won": 0,
                        "Lose": 0,
                        "Total": 0,
                        "red": 0,
                        "blue": 0,
                        "green": 0,
                        "marine": 0,
                        "orange": 0,
                        "pink": 0,
                        "purple": 0,
                        "yellow": 0,
                        "Best time": 1000000000
                    }

                    json.dump(empty_stats, f)

    def update_records(self):
        if self.info.is_over:
            for player in self.players:
                player_stats = {}
                with open('records/players/{0}.txt'.format(player.name), 'r') as f:
                    player_stats = json.load(f)
                    if player.name == self.winner.name:
                        player_stats['Won'] += 1
                    else:
                        player_stats['Lose'] += 1
                    player_stats['Total'] += 1
                    player_stats[player.color[0]] += 1
                    if self.time and player_stats['Best time'] > int(self.timers[player.name]) and player is PlayerMan:
                        player_stats['Best time'] = int(self.timers[player.name])
                with open('records/players/{0}.txt'.format(player.name), 'w+') as f:
                    json.dump(player_stats, f)

    def draw(self):
        window = self.info.window
        matrix = self.info.game_matrix
        window.fill(Colors.gray)
        y1 = matrix[0][0].y
        y2 = matrix[0][-1].y
        x1 = matrix[0][0].x
        x2 = matrix[-1][0].x
        d = self.info.dot_size
        for x in [x[0].x + d / 2 for x in matrix]:
            pygame.draw.line(window, (140, 140, 140), (x, y1), (x, y2 + d), 3)

        for y in [y.y + d / 2 for y in matrix[0]]:
            pygame.draw.line(window, (140, 140, 140), (x1, y), (x2 + d, y), 3)

        for lay in matrix:
            for dot in lay:
                if dot.is_active():
                    window.blit(dot.image[0], (dot.x, dot.y))
                else:
                    window.blit(dot.image[1], (dot.x, dot.y))

        for b in [x[1] for x in self.buttons.items()]:
            if b.image is not None:
                window.blit(b.image, b.cords)

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 16)
        if not self.info.is_over:
            window.blit(font.render("It's     's turn", True, Colors.black), (490, 10))
            window.blit(self.players[self.order].color[1][0], (513, 12))
        else:
            window.blit(font.render("{0} won".format(self.winner.name), True, Colors.black), (490, 10))
            window.blit(self.winner.color[1][0], (513, 12))

        font = pygame.font.SysFont('Arialblack', 16)
        x = self.info.res[0] - 200
        y = 30
        for player in self.players:
            window.blit(font.render('{0}: {1}'.format(player.name, player.points), True, self.colors[player.color[0]]),
                        (x, y))
            if self.time:
                window.blit(font.render("%.2f" % self.timers[player.name], True, Colors.black), (x - 40, y))
            y += 40

        pygame.display.update()

    def click_action(self, m_pos):
        # print(m_pos)
        d = self.info.dot_size
        pos = (-1, -1)
        for i in range(self.info.field[0]):
            for j in range(self.info.field[1]):
                if self.info.game_matrix[i][j].x - 2 <= m_pos[0] <= self.info.game_matrix[i][j].x + d + 2 and \
                        self.info.game_matrix[i][j].y - 2 <= m_pos[1] <= self.info.game_matrix[i][j].y + d + 2:
                    pos = (i, j)

        return pos

    def make_move(self):
        if self.info.is_over:
            return
        p = self.players[self.order]
        d = p.make_move(self.info.game_matrix)
        dot = self.info.game_matrix[d[0]][d[1]]
        if dot.color == 'gray':
            self.info.game_matrix[d[0]][d[1]].change_color(p.color)
            disabled, active = Referee.check_surrounded(self.info.game_matrix, p.color[0])
            p.points = len(disabled)
            for pos in disabled:
                self.info.game_matrix[pos[0]][pos[1]].active = False
            self.counter += 1
            if self.counter == len(self.info.game_matrix) * len(self.info.game_matrix[0]):
                self.winner = sorted(self.players, key=lambda p: p.points, reverse=True)[0]
                self.info.is_over = True
                self.update_records()

            if self.order + 1 == len(self.players):
                self.order = 0
            else:
                self.order += 1

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.over = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                index = self.click_action(e.pos)
                if index == (-1, -1):
                    self.handle_events_buttons(e.pos)
                else:
                    self.handle_events_players(index)

    def handle_events_buttons(self, m_pos):
        for b in [x[1] for x in self.buttons.items()]:
            if b.is_pressed(m_pos):
                b.on_click()
                break

    def handle_events_players(self, index):
        if self.info.game_matrix[index[0]][index[1]].is_active():
            self.players[self.order].dot_coords = index
            self.make_move()

    def handle_events_enter_text(self, name):
        is_over = False
        text = name.split()
        while not is_over:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.over = True
                    return
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons['Save'].is_pressed(e.pos):
                        is_over = True
                elif e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        pygame.display.set_caption('Dots')
                        return
                    elif e.key == pygame.K_RETURN:
                        is_over = True
                    elif e.key == pygame.K_BACKSPACE:
                        if len(text) > 0:
                            text.pop()
                    elif not e.key == pygame.K_MINUS:
                        text += e.unicode

            pygame.display.set_caption('Save as ' + ''.join(text))

        return ''.join(text)
