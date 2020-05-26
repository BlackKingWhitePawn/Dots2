import os
import pygame
from colors import Colors
from button import Button
from saveLoad import load
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

        self.buttons = {

        }

        y = 10
        for s in os.listdir('saves'):
            self.buttons.update({
                s: Button((10, y), (200, 65), lambda: load(s), Images.empty),
                s + '-d': Button((220, y), (65, 65), create_delete_func(s), Images.cross)
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

        pygame.font.init()
        font = pygame.font.SysFont('Arial', 40)
        for k, v in self.buttons.items():
            if not k[-2:] == '-d':
                self.window.blit(font.render(k[:-4], True, Colors.gray), v.cords)

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

    # def update_buttons(self):
    #     y = 10
    #     for k, v in self.buttons.items():
    #         x = v.cords[0]
    #         v.cords = (x, y)
    #         y += 80
