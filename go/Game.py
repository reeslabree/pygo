import pygame, sys, copy
import time
from copy import deepcopy
from .Board import Board
from .constants import FPS, WIN_DIM_X, WIN_DIM_Y, WHITE
from .constants import BUTTON_NULL, BUTTON_PASS, BUTTON_RESIGN, BUTTON_SAVE, BUTTON_UNDO
from .Button import Button
from .Memento import Memento, Caretaker, ConcreteMemento, Originator

class Game:
    def __init__(self,
                 dimension,
                 starting_player,
                 starting_white,
                 starting_black,
                 should_load=False) -> object:

        pygame.init()
        self.window = pygame.display.set_mode((WIN_DIM_X, WIN_DIM_Y))
        self.clock = pygame.time.Clock()

        self.pass_flag = False

        self.white_score = 0
        self.black_score = 0
        self.board = Board(self.window, dimension, starting_white, starting_black)
        self.state = ['update', 'wait']  # queue of events
        self.player = starting_player
        self.window.fill(WHITE)

        # memento implementation
        self.originator = Originator(self._get_memento_state())
        self.caretaker = Caretaker(self.originator)
        if not should_load:
            self.caretaker.backup()
        else:
            self.caretaker.read_file()
            self.state.append('undo')

    # gathers the current status of the Game object and packs into a dictionary
    # this dictionary serves as a 'memento state', not to be confused with a 'state machine state'
    def _get_memento_state(self):
        mem_state = {
                'white_score': self.white_score,
                'black_score': self.black_score,
                'board': deepcopy(self.board.get_board()),
                'state_queue': self.state,
                'player': self.player
                }
        return mem_state

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
                    if self.pass_flag:
                        self.state = ['end', 'wait'] 
                    else:
                        self.pass_flag = True
                    if self.player == 'black':
                        self.player = 'white'
                    else:
                        self.player = 'black'
                elif click == BUTTON_RESIGN:
                    print('resign')
                    self.state.append('quit')
                elif click == BUTTON_SAVE:
                    self.state.append('save')
                    self.state.append('wait')
                elif click == BUTTON_UNDO:
                    self.state.append('undo')
                    self.state.append('wait')
                    print('undo')
                    return
            self.caretaker.backup()
            if self.board.place(pos, self.player) == False:
                #if fail, pop the backup
                self.caretaker.undo()

                # alert that there was an invalid placement
                print('invalid placement')  # TODO: make this do a pop up or something

            else:
                # valid token placement
                self.pass_flag = False
                if self.player == 'white':
                    self.player = 'black'
                else:
                    self.player = 'white'
                self.state.append('capture')
                self.state.append('check_win')
                self.state.append('update')
                
            self.state.append('wait')

        else:
            self.state.append('wait')

        self.originator.update_state(self._get_memento_state())

    def _capture(self):
        score = self.board.try_capture(self.player)
        if self.player == 'white':
            self.black_score += score
        else:
            self.white_score += score

    def _update(self):
        print(self.state) #TODO remove me
        self.board.update_board(self.white_score, self.black_score)
        pygame.display.update()

    def _score(self):
        self.black_score, self.white_score = self.board.score_game()

    def _save_mem(self):
        self.caretaker.backup()
        self.caretaker.show_history()   # using this for testing

    def _undo(self):
        # tell the caretaker to pop the last saved state and save it to the originator
        if not self.caretaker.undo():
            return

        # return the originator's old state
        recall = self.originator.current_state()

        # update the game values
        self.white_score = recall['white_score']
        self.black_score = recall['black_score']
        self.board.set_board(recall['board'])
        self.state = recall['state_queue']
        self.player = recall['player']

        self.state.insert(0, 'update')

    def _save_game(self):
        self.caretaker.show_history()
        self.caretaker.write_file()

    def _display_winner(self):
        print('displaying winner')
        if self.white_score > self.black_score:
            text = 'White Wins'
        elif self.black_score > self.white_score:
            text = 'Black Wins'
        else:
            text = 'Draw'

        self.window.fill(WHITE)
        font = pygame.font.SysFont('Arial', 150)
        text_surface = font.render(text, False, (0,0,0))
        center = (WIN_DIM_X // 5, WIN_DIM_Y // 5)
        self.window.blit(text_surface, center)
        pygame.display.update()

    def go(self):
        self.board.update_board(self.white_score, self.black_score)
        while True:
            next_state = self.state.pop(0)
            if next_state == 'wait':
                self._wait()

            elif next_state == 'update':
                self._update()

            elif next_state == 'check_win':
                self._score()

            elif next_state == 'capture':
                self._capture()

            elif next_state == 'save':
                self._save_game()
                print('save game')

            elif next_state == 'save_mem':
                self._save_mem()

            elif next_state == 'undo':
                self._undo()

            elif next_state == 'end':
                self._display_winner()
            
            elif next_state == 'quit':
                exit()
                break
