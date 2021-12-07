import pygame, sys, copy
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

        # memento implementation
        self.originator = Originator(self._get_memento_state())
        self.caretaker = Caretaker(self.originator)
        self.caretaker.backup()

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
                    if self.player == 'black':
                        self.player = 'white'
                    else:
                        self.player = 'black'
                elif click == BUTTON_RESIGN:
                    print('resign')
                    self.state.append('quit')
                elif click == BUTTON_SAVE:
                    print('save')
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
            
            else:   # valid token placement
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

        self.originator.update_state(self._get_memento_state())

    def _capture(self):
        score = self.board.try_capture(self.player)
        if self.player == 'white':
            self.black_score += score
        else:
            self.white_score += score

    def _update(self):
        print(self.state) #TODO remove me
        self.board.update_board()
        pygame.display.update()

    def _check_win(self):
        winner = self.board.check_win()

        if winner != None:
            print(winner)

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

            elif next_state == 'save_mem':
                self._save_mem()

            elif next_state == 'undo':
                self._undo()

            elif next_state == 'quit':
                exit()
                break
