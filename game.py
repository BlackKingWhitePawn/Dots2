import pygame
import threading
from gameInfo import GameInfo
from playerMan import PlayerMan
from playerBot import PlayerBot
from images import Images
from button import Button
from colors import Colors


class Game:

    def __init__(self, res, data):
        pygame.init()
        self.info = GameInfo((data["n_x"], data['n_y']), res)
        self.players = [PlayerMan(x) for x in data["men_images"]] + [PlayerBot(x) for x in data["ai_images"]]
        self.order = 0
        self.data = {"new_game": False}

        def over():
            self.info.is_over = True

        def restart():
            self.info.window.fill(Colors.gray)
            self.order = 0
            self.info.game_matrix = self.info.init_matrix(self.info.field)

        def new_game():
            self.data["new_game"] = True
            over()

        self.buttons = {
            'Restart': Button((40, 10), (20, 20), restart, Images.restart),
            'New Game': Button((10, 10), (20, 20), new_game, Images.home),
            'Record table': Button((70, 10), (20, 20), lambda: None, Images.record)
        }

    '''main loop'''

    def run(self):
        self.draw()
        while not self.info.is_over:
            if type(self.players[self.order]) is PlayerBot:
                self.make_move()
            else:
                self.handle_events()

            self.draw()

    def start(self):
        pass

    def draw(self):
        self.info.window.fill(Colors.gray)
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
                self.info.window.blit(dot.image, (dot.x, dot.y))

        for b in [x[1] for x in self.buttons.items()]:
            if b.image is not None:
                self.info.window.blit(b.image, b.cords)

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 16)
        self.info.window.blit(font.render("It's     's turn", False, Colors.black), (500, 10))
        self.info.window.blit(self.players[self.order].color, (523, 12))

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
