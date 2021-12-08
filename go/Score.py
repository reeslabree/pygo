########################################################################################################################
# For Score keeping, reference used:  https://github.com/brilee/go_implementation/blob/master/go_naive.py
#                                     https://exercism.org/tracks/python/exercises/go-counting/solutions/CFred
# Strategy pattern:  https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_strategy.htm
########################################################################################################################
from .constants import BL, WH, NO
from abc import ABC, abstractmethod
import types
import numpy as np


########################################################################################################################
# Default scoring for Go is only territories captured.  Strategy implements capture score keeping.
# Implementing captured scoring with strategy pattern
########################################################################################################################
class Strategy(ABC):
    @abstractmethod
    def calculate_score(self):
        pass


class Score:
    def __init__(self, dimension) -> None:
        self.board = [[' '] * dimension for i in range(dimension)]
        self.columns = len(self.board[0])
        self.rows = len(self.board)
        self.black_captured = 0
        self.white_captured = 0
        self._strategy = None

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
            self._strategy = strategy

    def update(self, color, x, y) -> None:
        if color is 'black':
            self.board[y - 1][x - 1] = BL
        elif color is 'white':
            self.board[y - 1][x - 1] = WH
        else:
            if self.board[y - 1][x - 1] is BL:
                self.black_captured += 1
                # print("Black Captured: ", self.black_captured)
            elif self.board[y - 1][x - 1] is WH:
                self.white_captured += 1
                # print("White Captured: ", self.white_captured)
            self.board[y - 1][x - 1] = NO
        # DEBUG
        # print(np.matrix(self.board))

    def valid_space(self, x, y):
        return 0 <= y < self.rows and 0 <= x < self.columns

    def space(self, x, y):
        return self.board[y][x]

    def territory(self, x, y):
        def grow_territory(x1, y1):
            nonlocal territory
            if (x1, y1) in territory:
                return
            territory.add((x1, y1))
            for n in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x2 = x1 + n[0]
                y2 = y1 + n[1]
                if self.valid_space(x2, y2) and self.space(x2, y2) == NO:
                    grow_territory(x2, y2)

        if not self.valid_space(x, y):
            raise ValueError('Invalid coordinate')
        if self.space(x, y) != NO:
            return NO, set()
        for y1 in range(y - 1, -1, -1):
            if self.space(x, y1) != NO:
                owner = self.space(x, y1)
                break
        else:
            for y1 in range(y + 1, self.rows):
                if self.space(x, y1) != NO:
                    owner = self.space(x, y1)
                    break
            else:
                for x1 in range(x + 1, self.columns):
                    if self.space(x1, y) != NO:
                        owner = self.space(x1, y)
                        break
                else:
                    for x1 in range(x - 1, -1, -1):
                        if self.space(x1, y) != NO:
                            owner = self.space(x1, y)
                            break
                    else:
                        owner = NO
        territory = set()
        grow_territory(x, y)
        try:
            for space in territory:
                for n in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    xt = space[0] + n[0]
                    yt = space[1] + n[1]
                    if self.valid_space(xt, yt) and self.space(xt, yt) not in [owner, NO]:
                        owner = NO
                        raise StopIteration
        except StopIteration:
            pass
        return owner, territory

    def calculate_score(self) -> list:
        # Find the owners and the territories of the whole board
        scores = {WH: set(), BL: set(), NO: set()}
        for x in range(self.columns):
            for y in range(self.rows):
                if self.space(x, y) == NO and (x, y) not in set().union(*scores.values()):
                    owner, terr = self.territory(x, y)
                    if owner and terr:
                        scores[owner] = scores[owner].union(terr)
        score = []
        for k, v in scores.items():
            score.append(len(v))

        return score


class ScoreCaptured(Strategy):
    # Find the owners and the territories of the whole board
    def calculate_score(self) -> list:
        scores = {WH: set(), BL: set(), NO: set()}
        for x in range(self.columns):
            for y in range(self.rows):
                if self.space(x, y) == NO and (x, y) not in set().union(*scores.values()):
                    owner, terr = self.territory(x, y)
                    if owner and terr:
                        scores[owner] = scores[owner].union(terr)
        score = []
        for k, v in scores.items():
            score.append(len(v))
        score[0] += self.black_captured
        score[1] += self.white_captured

        return score
