import json
import os

import pygame
from dots.colors import Colors


class RecordWindow:
    def __init__(self):
        self.window = pygame.display.set_mode((1000, 600))
        self.buttons = {}
        self.is_over = False
        self.table = self.load_table()
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

    def init_window(self):
        self.window = pygame.display.set_mode((1920, 1080))
        self.window.fill(Colors.gray)
        pygame.display.set_caption('Record table')
        pygame.init()

    def run(self):
        self.init_window()
        self.is_over = False
        self.draw()
        while not self.is_over:
            self.draw()
            self.handle_events()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_over = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.handle_events_buttons(e.pos)

    def handle_events_buttons(self, m_pos):
        for b in [x[1] for x in self.buttons.items()]:
            if b.is_pressed(m_pos):
                b.on_click()
                break

    def draw(self):
        self.window.fill(Colors.gray)
        for k, v in self.buttons.items():
            pygame.font.init()
            size = min(max(10, 40 - 4 * (len(v.caption) - 10)), 40)
            font = pygame.font.SysFont('Arial', size)
            self.window.blit(font.render(v.caption, True, Colors.gray), (v.cords[0] + 15, v.cords[1] + 10))

        pygame.font.init()
        self.draw_table(self.table)
        pygame.display.update()

    def draw_table(self, table):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 28)
        x = 100
        y = 100
        first = True
        first2 = True
        for items in table.items():
            self.window.blit(font.render(items[0], True, Colors.black), (x, y))
            if first2:
                x += 200
                first2 = False
            for items2 in items[1].items():
                if first:
                    y -= 40
                    if items2[0] in self.colors:
                        self.window.blit(font.render(items2[0], True, self.colors[items2[0]]), (x, y))
                    else:
                        self.window.blit(font.render(items2[0], True, Colors.black), (x, y))

                    y += 40

                self.window.blit(font.render(items2[1].__str__(), True, Colors.black), (x, y))
                x += 80

            first = False
            first2 = True
            x = 100
            y += 40

    def load_table(self):
        table = {}
        for file_name in os.listdir('records/players'):
            with open('records/players/{}'.format(file_name), 'r') as f:
                table.update({file_name[:-4]: json.load(f)})

        return table
