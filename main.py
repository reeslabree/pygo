import pygame, sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
# import go.game
from go.board import Board
from go.constants import WINDOW_DIMENSION, WHITE, GRID_DIMENSION

pygame.display.set_caption('PyGo')

# TODO - move all this to the game function
def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))
    clock = pygame.time.Clock()
    window.fill(WHITE)
    
    board = Board(window, GRID_DIMENSION)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.place(pos, 'white')
    
        pygame.display.update()

main()
