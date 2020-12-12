import pygame

from controls.button import Button
from dots.colors import Colors
from images import Images
from player.playerMan import PlayerMan
from player.playerBot import PlayerBot


class PlayerWindow:
    def __init__(self, men_images, ai_images):
        self.buttons = {}
        i = 0
        self.player_men = []
        for x in men_images.items():
            i += 1
            self.player_men.append(PlayerMan(x, 'Player{0}'.format(i)))
        self.player_bot = []
        for x in ai_images.items():
            i += 1
            self.player_bot.append(PlayerBot(x, 'Player{0}'.format(i)))
        self.is_over = False
        self.back = False

        def create_change_name_func(button):
            def on_click():
                button.image = Images.empty_pressed
                self.draw()
                self.handle_events_enter_text(button)
                button.image = Images.empty
                self.draw()
            return on_click

        def create_button(cords, size, player):
            b = Button(cords, size, caption=player.name)
            b.on_click = create_change_name_func(b)
            return b

        y = 10
        for p in self.player_men:
            y1 = y
            self.buttons.update({
                p.name: create_button((10, y1), (200, 65), p)
            })
            y += 80
        for p in self.player_bot:
            y1 = y
            self.buttons.update({
                p.name: create_button((10, y1), (200, 65), p)
            })
            y += 80

        def back():
            self.is_over = True
            self.back = True

        def over():
            self.is_over = True

        height = max(600, (len(men_images) + len(ai_images) + 1) * 83)
        self.buttons.update({
            'back': Button((10, height - 90), (200, 65), on_click=back, caption='back to menu'),
            "OK": Button((220, height - 90), (150, 150), on_click=over, image=Images.play)
        })
        self.window = pygame.display.set_mode((300, height))
        self.window.fill(Colors.gray)
        pygame.display.set_caption('Set names to players')
        pygame.init()

    def run(self):
        self.draw()
        while not self.is_over:
            self.draw()
            self.handle_events()
        for k, v in self.buttons.items():
            for p in self.player_men + self.player_bot:
                if p.name == k:
                    p.name = v.caption
                    break

    def draw(self):
        self.window.fill(Colors.gray)
        for k, b in self.buttons.items():
            if b.image is not None:
                self.window.blit(b.image, b.cords)
            for p in self.player_bot + self.player_men:
                if p.name == k:
                    self.window.blit(p.color[1][0], (b.cords[0] + 215, b.cords[1] + 25))
                    break

        for k, v in self.buttons.items():
            pygame.font.init()
            size = min(max(10, 40 - 4 * (len(v.caption) - 10)), 40)
            font = pygame.font.SysFont('Arial', size)
            self.window.blit(font.render(v.caption, True, Colors.gray), (v.cords[0] + 15, v.cords[1] + 10))

        pygame.display.update()

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

    def handle_events_enter_text(self, button):
        is_over = False
        while not is_over:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.is_over = True
                    return
                elif e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        pygame.display.set_caption('Set names to players')
                        return
                    elif e.key == pygame.K_RETURN:
                        is_over = True
                    elif e.key == pygame.K_BACKSPACE:
                        if len(button.caption) > 0:
                            button.caption = button.caption[:-1]
                    elif not e.key == pygame.K_MINUS:
                        button.caption += e.unicode
                    self.draw()
