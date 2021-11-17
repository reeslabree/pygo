import pygame
from go.constants import TILE_B, TILE_W, BLACK, WHITE, WINDOW_DIMENSION

class Board:
    # constructor
    def __init__(self, window, dimension, white_start, black_start):
        self.dimension = dimension  # dimension of the board
        if white_start == None:
            self.white_pieces = []  # tuples of positions of the white pieces
        else:
            self.white_pieces = white_start
        if black_start == None:
            self.black_pieces = []  # tuples of positions of the black pieces
        else:
            self.black_pieces = black_start

        self.block_size = WINDOW_DIMENSION // (dimension + 1)
        self.win = window
        self._draw_grid()

    # draw the grid
    def _draw_grid(self):
        self.win.fill(WHITE)
        for x in range( self.block_size, 
                        WINDOW_DIMENSION - (self.block_size), 
                        self.block_size):
            for y in range( self.block_size, 
                            WINDOW_DIMENSION - (self.block_size), 
                            self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.win, BLACK, rect, 1)

    # draw a piece
    def _draw_piece(self, x, y, player):
        if player == 'white':
            color = TILE_W
        else:
            color = TILE_B

        center =   (x * self.block_size, 
                    y * self.block_size)
        pygame.draw.circle(self.win, color, center, (self.block_size // 2.25), 0)

    # check if there is a winner
    # TODO: implement
    def check_win(self):
        if False:
            return 'white'
        return None

    # clears the board, draw the pieces
    def update_board(self):
        self._draw_grid()
        for (x, y) in self.white_pieces:
            self._draw_piece(x, y, 'white')
        for (x, y) in self.black_pieces:
            self._draw_piece(x, y, 'black')

    # determines if a placement is a valid placement for a player
    ## returns 'True' if placement is valid
    ## returns 'False' if the placement is invalid
    def _is_invalid_placement(self, coord, player):
        # if there is a piece there already
        if coord in self.white_pieces + self.black_pieces:
            print('invalid: already placed')
            return False

        # if placement is surrounded by other player
        x, y = coord
        surrounding_coords = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for i, (a, b) in enumerate(surrounding_coords):
            if a<1 or b<1 or a>self.dimension or b>self.dimension:
                del surrounding_coords[i]
        if player == 'white' and set(surrounding_coords).issubset(set(self.black_pieces)):
            print('invalid: surrounded')
            return False
        elif player == 'black' and set(surrounding_coords).issubset(set(self.white_pieces)): 
            print('invalid: surrounded')
            return False

        # doesnt meet any of the above conditions = valid placement
        return True

    # place a piece adds a piece to the board
    ## returns 'True' if the placement is valid
    ## returns 'False' if the placement is invalid
    def place(self, pos, player):
        # turn pos on screen into row, col
        x, y = pos
        block_size = WINDOW_DIMENSION // (self.dimension + 2) 
        col = y // (block_size + 1)    
        row = x // (block_size + 1)
        
        # check if the x or y coord falls outside of the dimensions of the board
        if row in [0, self.dimension+1] or col in [0, self.dimension+1]:
            print('cannot place outside of the board')
            return False

        # check if valid placement, return False
        if not self._is_invalid_placement((row, col), player):
            return False

        # if valid placement, draw piece there, add to list of pieces
        if player == 'white':
            self.white_pieces.append((row, col))
        else:
            self.black_pieces.append((row, col))

        return True
