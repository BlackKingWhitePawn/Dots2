import pygame

from game.referee import Referee
from saveLoad import save
from game.gameInfo import GameInfo
from player.playerMan import PlayerMan
from player.playerBot import PlayerBot
from images import Images
from controls.button import Button
from dots.colors import Colors


class Game:

    def __init__(self, res, data, game_state=None):
        if game_state is not None:
            self.players = game_state['players']
            self.order = game_state['order']
            self.info = GameInfo((data["n_x"], data['n_y']), res, game_state['matrix'])
        else:
            self.players = [PlayerMan(x) for x in data["men_images"].items()] + [PlayerBot(x) for x in data["ai_images"].items()]
            self.order = 0
            self.info = GameInfo((data["n_x"], data['n_y']), res)
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

        def save_game():
            name = self.handle_events_enter_text('')
            result = save(self, 'saves/' + name + '.txt')
            while result is not None:
                pygame.display.set_caption(result)
                #time.sleep(1)
                name = self.handle_events_enter_text(name)
                result = save(self, 'saves/' + name + '.txt')
            pygame.display.set_caption(name + ' was saved')

        self.buttons = {
            'New Game': Button((10, 10), (20, 20), new_game, Images.home),
            'Restart': Button((40, 10), (20, 20), restart, Images.restart),
            'Record table': Button((70, 10), (20, 20), lambda: None, Images.record),
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
        while not self.info.is_over:
            if type(self.players[self.order]) is PlayerBot:
                #time.sleep(0.7)
                self.make_move()
            else:
                self.handle_events()

            self.draw()

    def start(self):
        pass

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
        window.blit(font.render("It's     's turn", True, Colors.black), (490, 10))
        window.blit(self.players[self.order].color[1][0], (513, 12))

        font = pygame.font.SysFont('Arialblack', 16)
        x = self.info.res[0] - 200
        y = 30
        for player in self.players:
            window.blit(font.render('{0}: {1}'.format(player.name, player.points), True, self.colors[player.color[0]]), (x, y))
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
        p = self.players[self.order]
        d = p.make_move(self.info.game_matrix)
        dot = self.info.game_matrix[d[0]][d[1]]
        if dot.color == 'gray':
            self.info.game_matrix[d[0]][d[1]].change_color(p.color)
            if self.order + 1 == len(self.players):
                self.order = 0
            else:
                self.order += 1
            disabled, active = Referee.check_surrounded(self.info.game_matrix, p.color[0])
            p.points = len(disabled)
            for pos in disabled:
                self.info.game_matrix[pos[0]][pos[1]].active = False

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

    def handle_events_enter_text(self, name):
        is_over = False
        text = name.split()
        while not is_over:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.info.is_over = True
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
