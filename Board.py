import numpy as np
import copy


class GameBoard:
    def __init__(self, rows_cols=3):
        self.cols = rows_cols
        self.rows = rows_cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.separator = "--+" + "---+" * (self.cols - 2) + "--"
        self.played_pos = []

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

        # check for tie game
        if np.count_nonzero(self.board) == self.rows * self.cols:
            return -1

        return 0

    def check_if_valid(self, pos):
        if isinstance(pos, int):
            pos = convert_to_position(pos, self.rows, self.cols)

        if isinstance(pos, tuple):
            if pos[0] > self.rows or pos[0] < 0 or \
                            pos[1] > self.cols or pos[1] < 0:
                return False
            if pos in self.played_pos:
                return False

        return self.board[pos[0], pos[1]] == 0


def convert_to_position(pos, rows, cols):
    return [int(pos / rows), pos % cols]


def look_ahead(board, player_turn):
    future_boards = []
    tmp_board = copy.copy(board)
    for c in range(board.cols):
        for r in range(board.rows):
            tmp_board.board = copy.copy(board.board)
            if tmp_board.check_if_valid((c, r)):
                tmp_board.board[c][r] = player_turn
                future_boards.append((copy.copy(tmp_board), (c, r)))

    return future_boards


def get_next_states(board, player_turn):
    future_boards = {}
    tmp_board = copy.copy(board)
    for c in range(board.cols):
        for r in range(board.rows):
            tmp_board.board = copy.copy(board.board)
            if tmp_board.check_if_valid((c, r)):
                tmp_board.board[c][r] = player_turn
                future_boards[(c, r)] = copy.copy(tmp_board)
    return future_boards
