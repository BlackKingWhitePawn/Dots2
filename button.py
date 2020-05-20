import pygame


class Button:
    def __init__(self, cords, size, color=(255, 255, 255), on_click=lambda *x: None, text=None):
        self.cords = cords
        self.size = size
        self.color = color
        self.on_click = on_click
        self.text = text

    def is_pressed(self, m_pos):
        return self.cords[0] <= m_pos[0] <= self.cords[0] + self.size[0] and \
               self.cords[1] <= m_pos[1] <= self.cords[1] + self.size[1]
