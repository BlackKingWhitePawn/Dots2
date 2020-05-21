from images import Images


class Dot:

    def __init__(self, ix=0, iy=0):
        self.image = Images.gray
        self.x = ix
        self.y = iy
        self.motioned = False

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)

    def change_color(self, color=None):
        if color == 'Red':
            self.image = Images.red
        else:
            self.image = Images.blue

        if color is not None:
            self.image = color

    def is_active(self):
        return self.image is Images.gray
