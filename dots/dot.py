from images import Images


class Dot:

    def __init__(self, ix=0, iy=0, image=Images.gray, color='gray'):
        self.active = True
        self.color = color
        self.image = image
        self.x = ix
        self.y = iy
        self.motioned = False

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y)

    def change_color(self, color):
        self.color = color[0]
        self.image = color[1]

    def is_active(self):
        return self.active
