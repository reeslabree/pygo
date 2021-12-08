import pygame


class Button:
    def __init__(self, text, pos, win, font, bg='black', feedback=''):
        self.x, self.y = pos
        self.font = pygame.font.SysFont('Arial', font)
        self.set_text(text, bg)
        self.win = win

    # set the text in the button s.t. the button is the size of the text
    def set_text(self, text, bg='white'):
        self.text = self.font.render(text, 1, pygame.Color('Black'))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0] * 1.2, self.size[1] * 1.2)

    # display the button
    def show(self):
        self.win.blit(self.surface, (self.x, self.y))

    # return whether or not the button has been clicked
    def click(self, pos):
        x, y = pos
        if self.rect.collidepoint(x, y):
            return True
        else:
            return False
