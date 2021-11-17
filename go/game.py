import pygame, sys
from .board import Board
from .constants import FPS, WINDOW_DIMENSION, WHITE

class Game:
    def __init__(self, 
                dimension=13, 
                starting_player='white', 
                starting_white=None, 
                starting_black=None):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))
        self.clock = pygame.time.Clock()

        self.board = Board(self.window, dimension, starting_white, starting_black)
        self.state = ['wait']
        self.player = starting_player
        self.window.fill(WHITE)

    def _wait(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.append('quit')
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.board.place(pos, self.player) == False:
                    # aler that there was an invalid placement
                    print('invalid placement')  #TODO: make this do a pop up or something
                else:
                    if self.player == 'white':
                        self.player == 'black'
                    else:
                        self.player == 'white'
                self.state.append('update')
                self.state.append('check_win')   
            else:
                self.state.append('wait')

    def _update(self): 
        self.board.update_board()
        pygame.display.update()
        self.state.append('wait')

    def _check_win(self):
        winner = self.board.check_win()

        if winner != None:
            print(winner)

        self.state.append('wait')

    def go(self):
        self.board.update_board()
        while True:
            try:
                next_state = self.state.pop(0)
            except:
                continue

            if next_state == 'wait':
                self._wait()

            elif next_state == 'update':
                self._update()
 
            elif next_state == 'check_win':
                self._check_win()

            elif next_state == 'save':
                # self.save_game()
                print('save game')

            elif next_state == 'quit':
                pygame.quit()
                break
