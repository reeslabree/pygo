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
    def draw_piece(self, x, y, player):
        if player == 'white':
            color = TILE_W
        else:
            color = TILE_B

        center =   (x * self.block_size + self.block_size, 
                    y * self.block_size + self.block_size)
        pygame.draw.circle(self.win, color, center, (self.block_size // 2.25), 0)

'''
    # draw the pieces
    def draw_pieces(block_size):
        for tile in self.white_pieces:

        for     

    # place a piece
    # pos = tuple <x,y>
    def place(self, pos):


    # return all valid <x,y> placements for player
    def _get_liberties(self, player):

    
    # check if pieces should be captured and remove them
    def capture(self):
    
'''

