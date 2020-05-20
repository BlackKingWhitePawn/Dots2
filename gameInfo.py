import pygame
from dot import Dot


class GameInfo(object):

    def __init__(self, field, res):
        self.space = 20
        self.dot_size = 12
        self.res = res
        self.window = pygame.display.set_mode(res)
        self.window.fill((192, 192, 192))
        self.is_over = False
        self.field_pos = ((res[0] - self.space * (field[0] - 1)) / 2, (res[1] - self.space * (field[1] - 1)) / 2)
        self.game_matrix = self.init_matrix(field)
        self.field = field

    def init_matrix(self, field):
        gm = list()
        for x in range(field[0]):
            gm.append(list())
            for y in range(field[1]):
                gm[x].append(Dot(x * self.space + self.field_pos[0], y * self.space + self.field_pos[1]))

        return gm
