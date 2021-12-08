import pygame
from go.constants import WIN_DIM_X, WIN_DIM_Y
from go.Menu import Menu

####
# STATE/Game Loop Pattern:  https://gameprogrammingpatterns.com/game-loop.html
#                           https://java-design-patterns.com/patterns/game-loop/
###
class StartGame:
    def __init__(self) -> object:
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = WIN_DIM_X, WIN_DIM_Y
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.menu = Menu(self)
        self.curr_menu = self.menu

    #
    # Main Gameplay Loop for Menu
    #
    def game_loop(self) -> None:

        while True:
            # Set Background Color
            self.menu.main_background()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main Menu
            if self.menu.main_menu.is_enabled():
                self.menu.main_menu.mainloop(self.menu.surface, self.menu.main_background)
            # Flip surface
            pygame.display.flip()
