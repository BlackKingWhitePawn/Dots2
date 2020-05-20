import pygame


class Button:
    def __init__(self, cords, size, color=(255, 255, 255), on_click=lambda *x: None, text=None):
        if not text is None:
            pygame.font.init()
            font = pygame.font.SysFont('Arial', round((size[0] - cords[0] - 4) / len(text)) + 10)
            self.text = font.render(text, False, (0, 0, 0))
        self.cords = cords
        self.size = size
        self.color = color
        self.on_click = on_click

    def is_pressed(self, m_pos):
        return self.cords[0] <= m_pos[0] <= self.cords[0] + self.size[0] and \
               self.cords[1] <= m_pos[1] <= self.cords[1] + self.size[1]
