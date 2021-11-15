import pygame, sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
# import go.game
from go.board import Board
from go.constants import WINDOW_DIMENSION, WHITE, GRID_DIMENSION

pygame.display.set_caption('PyGo')

def row_col(pos, dimension):
    x, y = pos
    block_size = WINDOW_DIMENSION // (dimension + 2) 
    row = y // (block_size + 1)    
    col = x // (block_size + 1)
    return row, col

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))
    clock = pygame.time.Clock()
    window.fill(WHITE)
    
    board = Board(window, GRID_DIMENSION)

    while True:
        board.draw_grid(window)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main()
