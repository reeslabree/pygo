import pygame
from go.constants import TILE_B, TILE_W, BLACK, WHITE, WINDOW_DIMENSION

class Board:
    # constructor
    def __init__(self, window, dimension):
        self.dimension = dimension  # dimension of the board
        self.white_pieces = []      # tuples of positions of the white pieces
        self.black_pieces = []      # tuples of positions of the black pieces
        self.block_size = WINDOW_DIMENSION // (dimension + 1)
        self.win = window
        self.draw_grid()

    # draw the grid
    def draw_grid(self):
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
        if player == 'white':
            if set(surrounding_coords).issubset(set(self.black_pieces)):
                print('invalid: surrounded')
                return False
        else:
            if set(surrounding_coords).issubset(set(self.white_pieces)):
                print('invalid: surrounded')
                return False

        # doesnt meet any of the above conditions = valid placement
        return True

    def place(self, pos, player):
        # turn pos on screen into row, col
        x, y = pos
        block_size = WINDOW_DIMENSION // (self.dimension + 2) 
        col = y // (block_size + 1)    
        row = x // (block_size + 1)

        # check if valid placement, return False
        if not self._is_invalid_placement((row, col), player):
            return False

        # if valid placement, draw piece there, add to list of pieces
        self._draw_piece(row, col, player)
        if player == 'white':
            self.white_pieces.append((row, col))
        else:
            self.black_pieces.append((row, col))

        return True
