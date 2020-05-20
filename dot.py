from colors import Colors


class Dot:

    def __init__(self, ix=0, iy=0):
        self.color = Colors.gray
        self.x = ix
        self.y = iy
        self.motioned = False

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)

    def change_color(self, color=None):
        if color == 'Red':
            self.color = Colors.red
        else:
            self.color = Colors.blue

        if color is not None:
            self.color = color

    def is_active(self):
        return self.color is Colors.gray
