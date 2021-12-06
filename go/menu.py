import pygame
import pygame_menu
from typing import Tuple, Any
from pygame_menu.examples import create_example_window
from .game import *
from .constants import WIN_DIM_X, WIN_DIM_Y

# CODE USED FOR EXAMPLE MENU TO GET STARTED:
# https://github.com/ppizarror/pygame-menu/blob/master/pygame_menu/examples/game_selector.py
# THIS CREATES THE MAIN MENU TO SELECT BOARD SIZE, OR LOAD A NEW GAME
#

class Menu:
    def __init__(self, game: object) -> None:
        self.DISPLAY_W, self.DISPLAY_H = WIN_DIM_X, WIN_DIM_Y
        self.surface = create_example_window('Example - Game Selector', (self.DISPLAY_W, self.DISPLAY_H))
        self.DIFFICULTY = ['EASY']
        self.player1 = 'Player 1'
        self.player2 = 'Player 2'
        self.play_menu = pygame_menu.Menu(
            height=self.DISPLAY_H,
            width=self.DISPLAY_W,
            title='Play Menu'
        )
        self.play_menu.add.selector('Select difficulty ',
                                    [('9x9', 'EASY'),
                                     ('13x13', 'MEDIUM'),
                                     ('19x19', 'HARD')],
                                    onchange=self.change_difficulty,
                                    selector_id='select_difficulty')
        self.player1 = self.play_menu.add.text_input('Player 1 (Black): ', default='Player 1')
        self.player2 = self.play_menu.add.text_input('Player 2 (White): ', default='Player 2')
        self.play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                                  self.start_the_game,
                                  #self.DIFFICULTY,
                                  #self.player1,
                                  #self.player2
                                  )
        self.play_menu.add.button('Return to Main Menu', pygame_menu.events.BACK)

        self.main_menu = pygame_menu.Menu(
            height=self.DISPLAY_H * 0.6,
            width=self.DISPLAY_W * 0.6,
            title='Main Menu',
            theme=pygame_menu.themes.THEME_DEFAULT.copy()
        )
        self.main_menu.add.button('Play', self.play_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def change_difficulty(self, value: Tuple[Any, int], difficulty: str) -> None:
        selected, index = value
        print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
        self.DIFFICULTY[0] = difficulty

    def main_background(self) -> None:
        self.surface.fill((128, 0, 128))

    def display_menu(self) -> None:
        font = pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30)

        assert isinstance(self.DIFFICULTY, list)
        difficulty = self.DIFFICULTY[0]
        assert isinstance(difficulty, str)

        if difficulty == 'EASY':
            f = font.render('9x9', True, (255, 255, 255))
        elif difficulty == 'MEDIUM':
            f = font.render('13x13', True, (255, 255, 255))
        elif difficulty == 'HARD':
            f = font.render('19x19', True, (255, 255, 255))
        else:
            raise ValueError(f'unknown difficulty {difficulty}')
        f_esc = font.render('Press ESC to open the menu', True, (255, 255, 255))

        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # main_menu as the menu that will check all your input.
        self.main_menu.disable()
        self.main_menu.full_reset()

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

        self.main_menu.disable()
        self.main_menu.full_reset()
        Game(d, 'black', None, None).go()

