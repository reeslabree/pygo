import pygame
import itertools
from collections import namedtuple
from go.constants import TILE_B, TILE_W, BLACK, WHITE, WIN_DIM_X, WIN_DIM_Y
from go.constants import BUTTON_NULL, BUTTON_PASS, BUTTON_RESIGN, BUTTON_SAVE, BUTTON_UNDO
from .Button import Button
from .Score import *


#############################################################################
# Create the Board object
# For Score keeping, used https://github.com/brilee/go_implementation/blob/master/go_naive.py
#############################################################################
class Board:
    # constructor
    def __init__(self, window, dimension, white_start, black_start, strategy):
        self.dimension = dimension  # dimension of the board
        if white_start is None:
            self.white_pieces = []  # tuples of positions of the white pieces
        else:
            self.white_pieces = white_start
        if black_start is None:
            self.black_pieces = []  # tuples of positions of the black pieces
        else:
            self.black_pieces = black_start
        # Establish Empty Board for Score Keeping (

        self.block_size = WIN_DIM_Y // (dimension + 1)
        self.win = window
        pos_pass = ((WIN_DIM_X - 400), ((4.375 * WIN_DIM_Y / 8)))
        self.button_pass = Button('Pass', pos_pass, self.win, 100, bg='white', feedback='pass')
        pos_resign = ((WIN_DIM_X - 400), (5.375 * (WIN_DIM_Y / 8)))
        self.button_resign = Button('Resign', pos_resign, self.win, 100, bg='white', feedback='resign')
        pos_save = ((WIN_DIM_X - 400), (6.375 * (WIN_DIM_Y / 8)))
        self.button_save = Button('Save', pos_save, self.win, 100, bg='white', feedback='save')
        pos_undo = ((WIN_DIM_X - 400), (3.375 * (WIN_DIM_Y / 8)))
        self.button_undo = Button('Undo', pos_undo, self.win, 100, bg='white', feedback='undo')
        self._draw_grid()
        
        self.scoreboard = Score(dimension, ScoreTerritory())
        # Toggle counting prisoners
        self.strategy = strategy
        if self.strategy:
            self.scoreboard.strategy = ScoreCaptured()
        self.blackScore = 0
        self.whiteScore = 0

    def get_board(self):
        ret = {
            'dimension': self.dimension,
            'white_pieces': self.white_pieces,
            'black_pieces': self.black_pieces,
            'scoreboard': self.scoreboard,
            'strategy': self.strategy
        }
        return ret

    def set_board(self, recall):
        self.dimension = recall['dimension']
        self.white_pieces = recall['white_pieces']
        self.black_pieces = recall['black_pieces']
        self.scoreboard = recall['scoreboard']
        self.strategy = recall['strategy']

    def check_button_click(self, pos):
        if self.button_pass.click(pos):
            return BUTTON_PASS
        elif self.button_resign.click(pos):
            return BUTTON_RESIGN
        elif self.button_save.click(pos):
            return BUTTON_SAVE
        elif self.button_undo.click(pos):
            return BUTTON_UNDO
        else:
            return BUTTON_NULL

    # draw the grid
    def _draw_grid(self):
        self.win.fill(WHITE)
        for x in range(self.block_size,
                       WIN_DIM_Y - (self.block_size),
                       self.block_size):
            for y in range(self.block_size,
                           WIN_DIM_Y - (self.block_size),
                           self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.win, BLACK, rect, 1)
        self.button_pass.show()
        self.button_resign.show()
        self.button_save.show()
        self.button_undo.show()

    # draw a piece
    def _draw_piece(self, x, y, player):
        if player is 'white':
            color = TILE_W
        else:
            color = TILE_B

        center = (x * self.block_size,
                  y * self.block_size)
        pygame.draw.circle(self.win, color, center, (self.block_size // 2.25), 0)

    # check if there is a winner
    def score_game(self):
        score = self.scoreboard.territories()
        self.blackScore = score[1]
        self.whiteScore = score[0]

        return self.blackScore, self.whiteScore

    # clears the board, draw the pieces
    def update_board(self, white, black):
        self._draw_grid()
        self._show_score(1200, 10, white, black)
        for (x, y) in self.white_pieces:
            self._draw_piece(x, y, 'white')
        for (x, y) in self.black_pieces:
            self._draw_piece(x, y, 'black')

    # determines if a placement is a valid placement for a player
    # returns 'True' if placement is valid
    # returns 'False' if the placement is invalid
    def _is_invalid_placement(self, coord):
        # if there is a piece there already
        if coord in self.white_pieces + self.black_pieces:
            print('invalid: already placed')
            return False

        # doesnt meet any of the above conditions = valid placement
        return True

    # checks if any pieces should be captured
    # returns list of tuples that should be captured
    def _is_captured(self, player, new_x, new_y):
        adjacent = []
        block = [(new_x, new_y)]
        to_capture = block.copy()

        if player == 'black':
            jeap = self.black_pieces
            safe = self.white_pieces
        else:
            jeap = self.white_pieces
            safe = self.black_pieces

        while len(block) > 0:
            (x, y) = block.pop(0)
            surrounding = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for coord in surrounding:
                if coord[0] < 1 or coord[0] > self.dimension or coord[1] < 1 or coord[1] > self.dimension:
                    continue

                if coord in jeap and coord not in to_capture:
                    block.append(coord)
                    to_capture.append(coord)
                elif coord in jeap:
                    continue
                elif coord in safe:
                    adjacent.append(coord)
                else:
                    return None

        return to_capture

    # check if any of the players pieces should be captured
    def try_capture(self, player) -> None:
        score = 0
        if player == 'white':
            copy = self.white_pieces.copy()
            while len(copy) > 0:
                try_piece = copy.pop()
                kill = self._is_captured('white', try_piece[0], try_piece[1])
                if kill is not None:
                    for piece in kill:
                        self.white_pieces.remove(piece)
                        self.scoreboard.update(' ', int(piece[0]), int(piece[1]))

        elif player == 'black':
            copy = self.black_pieces.copy()
            while len(copy) > 0:
                try_piece = copy.pop()
                kill = self._is_captured('black', int(try_piece[0]), int(try_piece[1]))
                if kill is not None:
                    for piece in kill:
                        self.black_pieces.remove(piece)
                        self.scoreboard.update(' ', int(piece[0]), int(piece[1]))

    # place a piece adds a piece to the board
    # returns 'True' if the placement is valid
    # returns 'False' if the placement is invalid
    def place(self, pos, player):
        # turn pos on screen into row, col
        x, y = pos
        col = (y + 0.5 * self.block_size) // self.block_size
        row = (x + 0.5 * self.block_size) // self.block_size

        # check if the x or y coord falls outside of the dimensions of the board
        if row < 1 or row > self.dimension or col < 1 or col > self.dimension:
            print('cannot place outside of the board')
            return False

        # check if there is already a piece there
        if not self._is_invalid_placement((row, col)):
            return False

        # place piece, draw piece there, add to list of pieces
        if player == 'white':
            self.white_pieces.append((row, col))
        else:
            self.black_pieces.append((row, col))

        # check if valid placement, if not remove the piece and return False
        if self._is_captured(player, row, col) is not None:
            if player == 'white':
                self.white_pieces.remove((row, col))
            else:
                self.black_pieces.remove((row, col))
            return False
        self.scoreboard.update(player, int(row), int(col))
        return True

    def _show_score(self, x, y, white, black):
        font = pygame.font.Font('freesansbold.ttf', 32)
        score = font.render("Score :", True, (0, 0, 0))
        w = font.render("white: " + str(white), True, (0, 0, 0))
        b = font.render("black: " + str(black), True, (0, 0, 0))
        screen = self.win
        screen.blit(score, (x, y))
        screen.blit(w, (x, y + 32))
        screen.blit(b, (x, y + 64))
