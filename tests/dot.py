class Dot:

    def __init__(self, color='gray'):
        self.active = True
        self.color = color

    def change_color(self, color):
        self.color = color[0]

    def is_active(self):
        return self.active
