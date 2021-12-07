import pygame_menu
from typing import Tuple, Any
from pygame_menu.examples import create_example_window
from .Game import *
from .constants import WIN_DIM_X, WIN_DIM_Y


# Notes:
#   PYGAME_MENU EXAMPLE CODE USED FOR TEMPLATE MENU TO GET STARTED:
#   https://github.com/ppizarror/pygame-menu/blob/master/pygame_menu/examples/game_selector.py
#


########################################################################################################################
# Menu class - Establish board size (difficulty) and player names.
########################################################################################################################
class Menu:
    def __init__(self, game: object) -> None:
        ################################################################################################################
        # Defaults
        ################################################################################################################
        self.DISPLAY_W, self.DISPLAY_H = WIN_DIM_X, WIN_DIM_Y
        self.surface = create_example_window('Game of Go', (self.DISPLAY_W, self.DISPLAY_H))
        self.DIFFICULTY = ['EASY']
        self.player1 = 'Player 1'
        self.player2 = 'Player 2'
        self.ABOUT = ['Created for CSCI4448 using PyGame.',
                      'Authors:', 'Jon Wick', 'Rees Labree', 'Austin Cha']
        ################################################################################################################
        # Play Menu
        ################################################################################################################
        self.play_menu = pygame_menu.Menu(
            height=self.DISPLAY_H,
            width=self.DISPLAY_W,
            title='Play Menu'
        )
        self.player1 = self.play_menu.add.text_input('Player 1 (Black): ', default='Player 1')
        self.player2 = self.play_menu.add.text_input('Player 2 (White): ', default='Player 2')
        self.play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                                  self.start_the_game,
                                  # self.DIFFICULTY,
                                  # self.player1,
                                  # self.player2
                                  )
        self.play_menu.add.selector('Select difficulty ',
                                    [('1 - Easy', 'EASY'),
                                     ('2 - Medium', 'MEDIUM'),
                                     ('3 - Hard', 'HARD')],
                                    onchange=self.change_difficulty,
                                    selector_id='select_difficulty')
        self.play_menu.add.button('Return to Main Menu', pygame_menu.events.BACK)

        ################################################################################################################
        # About Menu
        ################################################################################################################
        self.about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.about_theme.widget_margin = (50, 0)
        self.about_menu = pygame_menu.Menu(
            height=self.DISPLAY_H * 0.5,
            theme=self.about_theme,
            width=self.DISPLAY_W * 0.7,
            title='About',
        )

        for count, about in enumerate(self.ABOUT):
            if count < 1:
                self.about_menu.add.label(about, align=pygame_menu.locals.ALIGN_CENTER, font_size=25)
            elif count == 1:
                self.about_menu.add.label(about, align=pygame_menu.locals.ALIGN_CENTER, font_size=25, margin=(50, 10))
            else:
                self.about_menu.add.label(about, align=pygame_menu.locals.ALIGN_CENTER, font_size=20, margin=(50, 0))
        self.about_menu.add.vertical_margin(30)
        self.about_menu.add.button('Return to menu', pygame_menu.events.BACK)

        ################################################################################################################
        # Main Menu
        ################################################################################################################
        self.main_menu = pygame_menu.Menu(
            height=self.DISPLAY_H * 0.6,
            width=self.DISPLAY_W * 0.6,
            title='Go - Main Menu',
            theme=pygame_menu.themes.THEME_DEFAULT.copy()
        )
        self.main_menu.add.button('Play', self.play_menu)
        self.main_menu.add.button('Load', self.load_the_game)
        self.main_menu.add.button('About', self.about_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    ####################################################################################################################
    # Function that toggles between 3 difficulty settings.
    ####################################################################################################################
    def change_difficulty(self, value: Tuple[Any, int], difficulty: str) -> None:
        selected, index = value
        print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
        self.DIFFICULTY[0] = difficulty

    ####################################################################################################################
    # Sets background color for main window.
    ####################################################################################################################
    def main_background(self) -> None:
        self.surface.fill((128, 128, 128))

    ####################################################################################################################
    # Load Game
    ####################################################################################################################
    def load_the_game(self) -> None:
        Game(9, 'black', None, None, should_load=True).go()

    ####################################################################################################################
    # Start game - pass settings to Game loop
    ####################################################################################################################
    def start_the_game(self) -> None:
        diff = self.DIFFICULTY[0]

        if diff == 'EASY':
            d = 9
        elif diff == 'MEDIUM':
            d = 13
        elif diff == 'HARD':
            d = 19
        else:
            raise ValueError(f'unknown difficulty {diff}')

        Game(d, 'black', None, None).go()
