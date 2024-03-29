import pygame
from loadWindow import LoadWindow
from runApplication.playerWindow import PlayerWindow
from controls.button import Button
from player.playerMan import PlayerMan
from player.playerBot import PlayerBot
from images import Images
from dots.colors import Colors


class StartWindow:

    def __init__(self):
        self.available_images = {
            'green': Images.green,
            'orange': Images.orange,
            'yellow': Images.yellow,
            'pink': Images.pink,
            'purple': Images.purple,
            'marine': Images.marine
        }
        self.men_images = {'green': Images.green}
        self.ai_images = {'red': Images.red, 'blue': Images.blue, }
        self.men_players = {}
        self.ai_players = {}
        self.is_over = False
        self.data = {
            "men_players": self.men_players,
            "ai_players": self.ai_players,
            "men_images": self.men_images,
            "ai_images": self.ai_images,
            "resolution_set": (1000, 600),
            "n_x": 4,
            "n_y": 4,
            "men": 1,
            "ai": 2,
            "close": False,
            'time': False
        }
        self.game_state = None
        self.window = pygame.display.set_mode(self.data['resolution_set'])

        def over():
            if self.data['men'] + self.data['ai'] > 1:
                self.is_over = True

        def set_names():
            pw = PlayerWindow(self.men_images, self.ai_images)
            pw.run()
            self.window = pygame.display.set_mode((1000, 600))
            if not pw.back:
                self.men_players = pw.player_men
                self.ai_players = pw.player_bot
                over()

        def load_game():
            lw = LoadWindow()
            lw.run()
            self.window = pygame.display.set_mode((1000, 600))
            if lw.play:
                set_names()
            if lw.loaded is not None:
                self.game_state = lw.loaded
                over()
            pygame.display.set_caption('Main menu')

        def ai_plus():
            if self.data['ai'] < 8 - self.data["men"]:
                self.data['ai'] += 1
                color = self.available_images.popitem()
                self.ai_images[color[0]] = color[1]
            else:
                self.data['ai'] = 8 - self.data["men"]

        def ai_minus():
            if self.data['ai'] > 0:
                self.data['ai'] -= 1
                color = self.ai_images.popitem()
                self.available_images[color[0]] = color[1]
            else:
                self.data['ai'] = 0

        def men_plus():
            if self.data['men'] < 8 - self.data["ai"]:
                self.data['men'] += 1
                color = self.available_images.popitem()
                self.men_images[color[0]] = color[1]
            else:
                self.data['men'] = 8 - self.data["ai"]

        def men_minus():
            if self.data['men'] > 0:
                self.data['men'] -= 1
                color = self.men_images.popitem()
                self.available_images[color[0]] = color[1]
            else:
                self.data['men'] = 0

        def x_plus():
            if self.data['n_x'] < 100:
                self.data['n_x'] += 1
            else:
                self.data['n_x'] = 100

        def x_minus():
            if self.data['n_x'] > 2:
                self.data['n_x'] -= 1
            else:
                self.data['n_x'] = 2

        def y_plus():
            if self.data['n_y'] < 100:
                self.data['n_y'] += 1
            else:
                self.data['n_y'] = 100

        def y_minus():
            if self.data['n_y'] > 2:
                self.data['n_y'] -= 1
            else:
                self.data['n_y'] = 2

        def create_timer_button():
            b = Button((400, 250), (200, 65), caption='Timer off')

            def on_click():
                if b.caption == 'Timer off':
                    b.caption = 'Timer on'
                    b.image = Images.empty_pressed
                    self.data['time'] = True
                elif b.caption == 'Timer on':
                    b.caption = 'Timer off'
                    b.image = Images.empty
                    self.data['time'] = False

            b.on_click = on_click
            return b

        self.buttons = {
            "Bot_Players": Button((10, 10), (150, 150), image=Images.ai),
            "Up1": Button((180, 10), (65, 65), ai_plus, image=Images.up),
            "Down1": Button((180, 95), (65, 65), ai_minus, image=Images.down),

            "Man_Players": Button((400, 10), (150, 150), image=Images.man),
            "Up2": Button((570, 10), (65, 65), men_plus, image=Images.up),
            "Down2": Button((570, 95), (65, 65), men_minus, image=Images.down),

            "Timer": create_timer_button(),

            "n_Y": Button((10, 440), (150, 150), image=Images.ny),
            "Up3": Button((180, 440), (65, 65), y_plus, image=Images.up),
            "Down3": Button((180, 525), (65, 65), y_minus, image=Images.down),

            "n_X": Button((400, 440), (150, 150), image=Images.nx),
            "Up4": Button((570, 440), (65, 65), x_plus, image=Images.up),
            "Down4": Button((570, 525), (65, 65), x_minus, image=Images.down),

            "Load": Button((800, 10), (150, 150), on_click=load_game, image=Images.load),
            "OK": Button((800, 440), (150, 150), on_click=set_names, image=Images.ok)
        }

    def init_window(self):
        self.window = pygame.display.set_mode(self.data['resolution_set'])
        self.window.fill((192, 192, 192))
        pygame.display.set_caption('Main menu')
        pygame.init()

    def run(self):
        self.init_window()
        self.is_over = False
        self.data['close'] = False
        self.draw()
        while not self.is_over:
            self.draw()
            self.handle_events()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_over = True
                # self.data["close"] = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.handle_events_buttons(e.pos)

    def handle_events_buttons(self, m_pos):
        for b in [x[1] for x in self.buttons.items()]:
            if b.is_pressed(m_pos):
                b.on_click()
                break

    def draw(self):
        self.window.fill(Colors.gray)
        x = 10
        y = 170
        for key in self.ai_images:
            self.window.blit(self.ai_images[key][0], (x, y))
            x += 20

        x = 400
        y = 170
        for key in self.men_images:
            self.window.blit(self.men_images[key][0], (x, y))
            x += 20

        for k, v in self.buttons.items():
            if v.image is not None:
                self.window.blit(v.image, v.cords)
            pygame.font.init()
            size = min(max(10, 40 - 4 * (len(v.caption) - 10)), 40)
            font = pygame.font.SysFont('Arial', size)
            self.window.blit(font.render(v.caption, True, Colors.gray), (v.cords[0] + 15, v.cords[1] + 10))

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 100)
        self.window.blit(font.render(self.data["ai"].__str__(), True, Colors.black), (255, 10))
        self.window.blit(font.render(self.data["men"].__str__(), True, Colors.black), (645, 10))
        self.window.blit(font.render(self.data["n_y"].__str__(), True, Colors.black), (255, 440))
        self.window.blit(font.render(self.data["n_x"].__str__(), True, Colors.black), (645, 440))
        pygame.display.update()
