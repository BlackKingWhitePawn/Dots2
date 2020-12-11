import os
import json
import pygame
from dots.colors import Colors
from controls.button import Button
from saveLoad import enformat_matrix
from saveLoad import format_data_to_players
from images import Images


class LoadWindow:

    def __init__(self):
        self.is_over = False
        self.loaded = None

        def create_delete_func(name_to_delete):
            def delete():
                for file_name in os.listdir('saves'):
                    if file_name == name_to_delete:
                        os.remove('saves/' + name_to_delete)
                del self.buttons[name_to_delete]
                del self.buttons[name_to_delete + '-d']

            return delete

        def create_load_func(file_to_load):
            def load_game():
                for file_name in os.listdir('saves'):
                    if file_name == file_to_load:
                        os.chdir('saves')
                        with open(file_to_load) as f:
                            game_state = json.load(f)
                            game_state['matrix'] = enformat_matrix(game_state['matrix'])
                            game_state['players'] = format_data_to_players(game_state['players'])
                            os.chdir('..')
                            return game_state

            return load_game

        self.buttons = {

        }

        y = 10
        for s in os.listdir('saves'):
            y1 = y
            s1 = s
            self.buttons.update({
                s1: Button((10, y1), (200, 65), create_load_func(s1), Images.empty),
                s1 + '-d': Button((220, y1), (65, 65), create_delete_func(s1), Images.cross)
            })
            y += 80

        self.window = pygame.display.set_mode((300, 600))
        self.window.fill(Colors.gray)
        pygame.display.set_caption('Load game')
        pygame.init()

    def run(self):
        self.draw()
        while not self.is_over:
            self.draw()
            self.handle_events()

    def draw(self):
        self.window.fill(Colors.gray)
        for b in [x[1] for x in self.buttons.items()]:
            if b.image is not None:
                self.window.blit(b.image, b.cords)

        for k, v in self.buttons.items():
            if not k[-2:] == '-d':
                pygame.font.init()
                size = min(max(10, 40 - 4 * (len(k[:-4]) - 10)), 40)
                font = pygame.font.SysFont('Arial', size)
                self.window.blit(font.render(k[:-4], True, Colors.gray), (v.cords[0] + 15, v.cords[1] + 10))

        pygame.display.update()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_over = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.handle_events_buttons(e.pos)

    def handle_events_buttons(self, m_pos):
        for b in [x[1] for x in self.buttons.items()]:
            if b.is_pressed(m_pos):
                self.loaded = b.on_click()
                if self.loaded is not None:
                    self.is_over = True
                    return
