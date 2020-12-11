import pygame


class Button:
    def __init__(self, cords, size, on_click=lambda *x: None, image=None):
        self.cords = cords
        self.size = size
        self.on_click = on_click
        self.image = image

    def is_pressed(self, m_pos):
        return self.cords[0] <= m_pos[0] <= self.cords[0] + self.size[0] and \
               self.cords[1] <= m_pos[1] <= self.cords[1] + self.size[1]
