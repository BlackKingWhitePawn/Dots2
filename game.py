import pygame
from gameInfo import GameInfo
from playerMan import PlayerMan
from playerBot import PlayerBot
from colors import Colors
from button import Button


class Game:

    def __init__(self, field, res):
        pygame.init()
        self.info = GameInfo(field, res)
        self.players = [PlayerMan(Colors.red), PlayerBot(Colors.blue)]
        self.order = 0

        def over():
            self.info.is_over = True

        def restart():
            self.info.window.fill((192, 192, 192))
            self.order = 0
            self.info.game_matrix = self.info.init_matrix(self.info.field)

        colors = {
            'Red': (255, 0, 0),
            'Blue': (0, 0, 255),
            'Green': (0, 255, 0)
        }
        self.buttons = {
            'Simple': Button((10, 10), (30, 12), colors['Red'], lambda: print('it pressed!')),
            'Simple2': Button((50, 10), (30, 12), colors['Blue'], lambda: print('hey buddy')),
            'Restart': Button((200, 10), (50, 40), colors['Green'], restart)
        }

    '''main loop'''
    def run(self):
        self.draw()
        while not self.info.is_over:
            if type(self.players[self.order]) is PlayerBot:
                self.make_move()
                pygame.draw.rect(self.info.window, (123, 213, 233), (400, 10, 10, 10))
            else:
                self.handle_events()

            self.draw()

    def start(self):
        pass

    def draw(self):
        y1 = self.info.game_matrix[0][0].y
        y2 = self.info.game_matrix[0][-1].y
        x1 = self.info.game_matrix[0][0].x
        x2 = self.info.game_matrix[-1][0].x
        d = self.info.dot_size
        for x in [x[0].x + d / 2 for x in self.info.game_matrix]:
            pygame.draw.line(self.info.window, (140, 140, 140), (x, y1), (x, y2 + d), 3)

        for y in [y.y + d / 2 for y in self.info.game_matrix[0]]:
            pygame.draw.line(self.info.window, (140, 140, 140), (x1, y), (x2 + d, y), 3)

        for lay in self.info.game_matrix:
            for dot in lay:
                self.info.window.blit(dot.color, (dot.x, dot.y))

        for b in [x[1] for x in self.buttons.items()]:
            pygame.draw.rect(self.info.window, b.color, b.cords + b.size)

        pygame.display.update()

    def click_action(self, m_pos):
        d = self.info.dot_size
        pos = (-1, -1)
        for i in range(self.info.field[0]):
            for j in range(self.info.field[1]):
                if self.info.game_matrix[i][j].x - 2 <= m_pos[0] <= self.info.game_matrix[i][j].x + d + 2 and \
                        self.info.game_matrix[i][j].y - 2 <= m_pos[1] <= self.info.game_matrix[i][j].y + d + 2:
                    pos = (i, j)

        return pos

    def make_move(self):
        p = self.players[self.order]
        d = p.make_move(self.info.game_matrix)
        self.info.game_matrix[d[0]][d[1]].change_color(p.color)
        if self.order + 1 == len(self.players):
            self.order = 0
        else:
            self.order += 1

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.info.is_over = True
            elif e.type == pygame.MOUSEMOTION:
                index = self.click_action(e.pos)
                if not index == (-1, -1) and \
                        self.info.game_matrix[index[0]][index[1]].is_active():
                    self.info.game_matrix[index[0]][index[1]].motioned = True
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
