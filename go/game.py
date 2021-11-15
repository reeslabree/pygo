import pygame
from board import Board
from constants import WINDOW_DIMENSION, BLACK

class Game:
    def __init__(self, dimension):
        self.board = Board(dimension)

    # draws the grid on the board
    def draw_board(self):
        block_size = WINDOW_DIMENSION // (self.board.dimension + 2)
        for x in range(block_size, WINDOW_DIMENSION - block_size, block_size):
            for y in range(block_size, WINDOW_DIMENSION - block_size, block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    # update the game blah blah
    def update(self):
        self.draw_board(self)

    # attempt to place a tile
    def place(self, row, col):
        print('Called Place()')
