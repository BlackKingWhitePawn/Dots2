import pygame
from button import Button
from colors import Colors


class StartWindow:

    def __init__(self, res):
        self.is_over = False
        self.checked_params = {"is_resolution_set": 0, "is_color_set": 0}
        self.data = {"resolution_set": (1080, 720), "color_set": Colors.red}

        def over():
            self.is_over = True

        def set_red():
            self.checked_params["is_color_set"] = 1
            self.data["color_set"] = Colors.red

        def set_blue():
            self.checked_params["is_color_set"] = 1
            self.data["color_set"] = Colors.blue

        self.buttons = {
            # 'Simple': Button((10, 10), (30, 12), colors['Red'], lambda: print('it pressed!')),
            # 'Simple2': Button((50, 10), (30, 12), colors['Blue'], lambda: print('hey buddy')),
            # 'Restart': Button((200, 10), (50, 40), colors['Green'], restart)
            # "StartGame": Button((10, 10), (30, 30), (255, 3, 3), over)
            "Red": Button((10, 10), (30, 30), (255, 3, 3), set_red, "red"),
            "Blue": Button((50, 10), (30, 30), (3, 3, 255), set_blue, "blue"),
        }

        self.window = pygame.display.set_mode(res)
        self.window.fill((192, 192, 192))
        pygame.init()

    def run(self):
        self.draw()
        while sum(self.checked_params.values()) == 0 and not self.is_over:
            self.draw()
            self.handle_events()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_over = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.handle_events_buttons(e.pos)

    def handle_events_buttons(self, m_pos):
        for b in [x[1] for x in self.buttons.items()]:
            if b.is_pressed(m_pos):
                b.on_click()
                break

    def draw(self):
        for b in [x[1] for x in self.buttons.items()]:
            pygame.draw.rect(self.window, b.color, b.cords + b.size)
            self.window.blit(b.text, b.cords + (2, 2))

        pygame.display.update()
