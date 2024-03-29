from player.player import Player


class PlayerMan(Player):

    def __init__(self, color, name="default", points=0):
        self.color = color
        self.name = name
        if not points == 0:
            self.points = points
        else:
            self.points = 0
        self.dot_coords = (-1, -1)
        self.is_man = True

    def make_move(self, game_matrix):
        return self.dot_coords
