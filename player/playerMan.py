from player.player import Player


class PlayerMan(Player):

    def __init__(self, color):
        self.color = color
        self.dot_coords = (-1, -1)
        self.is_man = True

    def make_move(self, game_matrix):
        return self.dot_coords
