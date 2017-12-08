import numpy as np

class GameBoard:
    def __init__(self, rows_cols=3):
        self.cols = rows_cols
        self.rows = rows_cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.separator = "--+" + "---+" * (self.cols - 2) + "--"

    def show_board(self):
        for r in range(self.rows):
            if r in [x for x in range(1, self.rows)]:
                print(self.separator)
            for c in range(self.cols):
                line_end = '\n' if c == self.cols-1 else ''
                print(self.board[r][c], end=line_end)
                if c in [x for x in range(self.cols-1)]:
                    print(" | ", end='')

    def check_for_win(self):
        # Vertical
        for c in range(self.cols):

            if self.board[0][c] != 0 and all(x == self.board[0][c] for x in self.board[:, c]):
                return self.board[0][c]

        # horizontal
        for r in range(self.rows):
            if self.board[r][0] != 0 and all(x == self.board[r][0] for x in self.board[r, :]):
                return self.board[r][0]

        # diagonal
        if self.board[0][0] != 0 and all(x == self.board[0][0] for x in np.diag(self.board)):
            return self.board[0][0]
        if self.board[self.rows-1][0] != 0 and all(x == self.board[self.rows-1][0] for x in np.diag(np.fliplr(self.board))):
            return self.board[self.rows-1][0]

        return 0

    def check_if_valid(self, pos):
        if pos[0] > self.rows or pos[0] < 0 or  \
                pos[1] > self.cols or pos[1] < 0:
            return False

        return self.board[pos[0], pos[1]] == 0
