import pygame, sys
from .board import Board
from .constants import FPS, WIN_DIM_X, WIN_DIM_Y, WHITE
from .constants import BUTTON_NULL, BUTTON_PASS, BUTTON_RESIGN, BUTTON_SAVE
from .button import Button


class Game:
    def __init__(self,
                 dimension,
                 starting_player,
                 starting_white,
                 starting_black) -> object:
        pygame.init()
        self.window = pygame.display.set_mode((WIN_DIM_X, WIN_DIM_Y))
        self.clock = pygame.time.Clock()

        self.white_score = 0
        self.black_score = 0
        self.board = Board(self.window, dimension, starting_white, starting_black)
        self.state = ['update', 'wait']  # queue of events
        self.player = starting_player
        self.window.fill(WHITE)

    def _wait(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.state.append('quit')

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            click = self.board.check_button_click(pos)
            if click != BUTTON_NULL:
                if click == BUTTON_PASS:
                    print('pass')
                    if self.player == 'black':
                        self.player = 'white'
                    else:
                        self.player = 'black'
                elif click == BUTTON_RESIGN:
                    print('resign')
                    self.state.append('quit')
                elif click == BUTTON_SAVE:
                    print('save')
            elif self.board.place(pos, self.player) == False:
                # aler that there was an invalid placement
                print('invalid placement')  # TODO: make this do a pop up or something
            else:
                if self.player == 'white':
                    self.player = 'black'
                else:
                    self.player = 'white'
                self.state.append('capture') 
            self.state.append('update')
            self.state.append('check_win')
            self.state.append('wait')
        else:
            self.state.append('wait')

    def _capture(self):
        score = self.board.try_capture(self.player)
        if self.player == 'white':
            self.black_score += score
        else:
            self.white_score += score

    def _update(self):
        self.board.update_board()
        pygame.display.update()
    def _check_win(self):
        winner = self.board.check_win()

        if winner != None:
            print(winner)

    def go(self):
        self.board.update_board()
        while True:
            next_state = self.state.pop(0)
            if next_state == 'wait':
                self._wait()

            elif next_state == 'update':
                self._update()

            elif next_state == 'check_win':
                self._check_win()

            elif next_state == 'capture':
                self._capture()

            elif next_state == 'save':
                # self.save_game()
                print('save game')

            elif next_state == 'quit':
                exit()
                break
