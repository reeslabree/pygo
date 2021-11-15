import pygame
import pygame_menu
from random import randrange
from typing import Tuple, Any, Optional, List
from pygame_menu.examples import create_example_window


# CODE USED FOR EXAMPLE MENU TO GET STARTED:
# https://github.com/ppizarror/pygame-menu/blob/master/pygame_menu/examples/game_selector.py
# THIS CREATES THE MAIN MENU TO SELECT BOARD SIZE, OR LOAD A NEW GAME
#

class Menu:
    def __init__(self, game):
        self.DISPLAY_W, self.DISPLAY_H = 720, 480
        self.surface = create_example_window('Example - Game Selector', (self.DISPLAY_W, self.DISPLAY_H))
        self.DIFFICULTY = ['EASY']
        self.play_menu = pygame_menu.Menu(
            height=self.DISPLAY_H,
            width=self.DISPLAY_W,
            title='Play Menu'
        )
        self.play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                                  self.display_menu,
                                  self.DIFFICULTY
                                  )
        self.play_menu.add.selector('Select difficulty ',
                                    [('1 - Easy', 'EASY'),
                                     ('2 - Medium', 'MEDIUM'),
                                     ('3 - Hard', 'HARD')],
                                    onchange=self.change_difficulty,
                                    selector_id='select_difficulty')
        self.play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

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

    def random_color(self) -> Tuple[int, int, int]:
        return randrange(0, 255), randrange(0, 255), randrange(0, 255)

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

        # Draw random color and text
        bg_color = self.random_color()

        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # main_menu as the menu that will check all your input.
        self.main_menu.disable()
        self.main_menu.full_reset()
