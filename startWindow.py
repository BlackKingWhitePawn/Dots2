import pygame
from button import Button
from images import Images
from colors import Colors


class StartWindow:

    def __init__(self, res):
        self.available_images = {
            Images.green,
            Images.orange,
            Images.yellow,
            Images.pink,
            Images.purple,
            Images.marine
        }
        self.men_images = [Images.red]
        self.ai_images = [Images.blue]
        self.is_over = False
        self.data = {
            "men_images": self.men_images,
            "ai_images": self.ai_images,
            "resolution_set": (1080, 720),
            "n_x": 32,
            "n_y": 39,
            "men": 1,
            "ai": 1,
            "close": False
        }

        def over():
            self.is_over = True

        def ai_plus():
            if self.data['ai'] < 8 - self.data["men"]:
                self.data['ai'] += 1
                self.ai_images.append(self.available_images.pop())
            else:
                self.data['ai'] = 8 - self.data["men"]

        def ai_minus():
            if self.data['ai'] > 0:
                self.data['ai'] -= 1
                self.available_images.add(self.ai_images.pop())
            else:
                self.data['ai'] = 0

        def men_plus():
            if self.data['men'] < 8 - self.data["ai"]:
                self.data['men'] += 1
                self.men_images.append(self.available_images.pop())
            else:
                self.data['men'] = 8 - self.data["ai"]

        def men_minus():
            if self.data['men'] > 0:
                self.data['men'] -= 1
                self.available_images.add(self.men_images.pop())
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

        self.buttons = {
            "Bot_Players": Button((10, 10), (150, 150), image=Images.ai),
            "Up1": Button((180, 10), (65, 65), ai_plus, image=Images.up),
            "Down1": Button((180, 95), (65, 65), ai_minus, image=Images.down),

            "Man_Players": Button((400, 10), (150, 150), image=Images.man),
            "Up2": Button((570, 10), (65, 65), men_plus, image=Images.up),
            "Down2": Button((570, 95), (65, 65), men_minus, image=Images.down),

            "n_Y": Button((10, 440), (150, 150), image=Images.ny),
            "Up3": Button((180, 440), (65, 65), y_plus, image=Images.up),
            "Down3": Button((180, 525), (65, 65), y_minus, image=Images.down),

            "n_X": Button((400, 440), (150, 150), image=Images.nx),
            "Up4": Button((570, 440), (65, 65), x_plus, image=Images.up),
            "Down4": Button((570, 525), (65, 65), x_minus, image=Images.down),

            "OK": Button((800, 225), (150, 150), on_click=over)
        }

        self.window = pygame.display.set_mode(res)
        self.window.fill((192, 192, 192))
        pygame.init()

    def run(self):
        self.draw()
        while not self.is_over:
            self.draw()
            self.handle_events()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_over = True
                self.data["close"] = True
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
        for n in self.ai_images:
            self.window.blit(n, (x, y))
            x += 20

        x = 400
        y = 170
        for n in self.men_images:
            self.window.blit(n, (x, y))
            x += 20

        for b in [x[1] for x in self.buttons.items()]:
            if b.image is not None:
                self.window.blit(b.image, b.cords)

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 100)
        self.window.blit(font.render(self.data["ai"].__str__(), False, Colors.black), (255, 10))
        self.window.blit(font.render(self.data["men"].__str__(), False, Colors.black), (645, 10))
        self.window.blit(font.render(self.data["n_y"].__str__(), False, Colors.black), (255, 440))
        self.window.blit(font.render(self.data["n_x"].__str__(), False, Colors.black), (645, 440))
        pygame.display.update()
