import pygame
from menu import *


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 720, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = 'src/8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.menu = Menu(self)
        #self.options = OptionsMenu(self)
        #self.credits = CreditsMenu(self)
        self.curr_menu = self.menu

    def game_loop(self):
        while True:

            # Paint background
            self.menu.main_background()

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main menu
            if self.menu.main_menu.is_enabled():
                self.menu.main_menu.mainloop(self.menu.surface, self.menu.main_background)

            # Flip surface
            pygame.display.flip()
