from Board import GameBoard, look_ahead, convert_to_position
import numpy as np
import NeuralNet as net

dict2list = lambda _dict: [x for x in _dict.values()]
rem_invalid = lambda _list: list(filter(lambda x: x != -np.inf, _list))


class Agent:
    def __init__(self, number, is_human, prediction_type=None):
        self.number = number
        self.is_human = is_human
        self.prediction_type = prediction_type
        if self.prediction_type == "q_learning":
            self.nn = net.NeuralNet([[81, 'relu'], [81, 'relu'], [9, 'relu']], 81)

    def move(self, board):
        value = {}
        for r in range(board.rows):
            for c in range(board.cols):
                value[(r, c)] = 0
        if self.is_human:
            pos = convert_to_position(int(input("Please type the position you would like to play: ")),
                                      board.rows,
                                      board.cols)
            while not board.check_if_valid(pos):
                pos = convert_to_position(int(input("That is not a valid move! Please try again: ")),
                                          board.rows,
                                          board.cols)
            board.played_pos.append(pos)
            return pos

        else:
            if self.prediction_type == "minimax":
                board_val = get_value_of_board_recursion([[[[board, (0, 0)]]]], self.number, value, 1, 3)
            elif self.prediction_type == "q_learning":
                board_val = self.nn.get_value_of_board_q_learning(board)
            else:
                raise Exception("Invalid prediction type %s" % self.prediction_type)
            possible_moves = get_best_action(board_val)
            if len(possible_moves) > 1:
                pos = possible_moves[np.random.choice(len(possible_moves))]
                while not board.check_if_valid(pos):
                    pos = possible_moves[np.random.choice(len(possible_moves))]
                board.played_pos.append(pos)
                return pos
            elif len(possible_moves) == 1:
                board.played_pos.append(possible_moves[0])
                return possible_moves[0]
            elif len(possible_moves) == 0:
                return None
            else:
                raise Exception("Something horrible has happened")


def get_value_of_board(board, current_player):
    value = {}
    next_player = 1 if current_player == 2 else 2
    for r in range(board.rows):
        for c in range(board.cols):
            value[(r, c)] = 0

    future_boards = [look_ahead(board, current_player), []]
    for b in future_boards[0]:
        winner = b[0].check_for_win()
        if winner == current_player:
            value[b[1]] += 10
        future_boards[1].append((b[1], look_ahead(b[0], 1 if current_player == 2 else 2)))
    for i in future_boards[1]:
        for b in i[1]:
            winner = b[0].check_for_win()
            if winner == next_player:  # This will choose the other player
                value[i[0]] -= 10
    return value


def get_value_of_board_recursion(future_boards, current_player, value, recursion, max_lookahead):
    future_boards.append(
        [look_ahead(each[0], current_player) for boards in future_boards[recursion-1] for each in boards]
    )

    for board in future_boards[recursion]:
        for each in board:
            winner = each[0].check_for_win()
            if winner == current_player:
                value[each[1]] += 10
            elif winner == 1 if current_player == 2 else 2:
                value[each[1]] -= 10
    if max_lookahead == recursion:
        for pos in future_boards[0][0][0][0].played_pos:
            pos = tuple(pos)
            value[pos] = -np.inf
        return value
    else:
        return get_value_of_board_recursion(future_boards,
                                            1 if current_player == 2 else 2,
                                            value,
                                            recursion+1,
                                            max_lookahead)


def get_best_action(value):
    """Parses a dict object and returns a list of all keys with max value.

        # Arguments
            value: a dict object where keys are (tuple) board positions and values are the associated 'reward'
                where -np.inf means the space is invalid

        # Returns
            A list of best positions based on 'reward', returns multiple positions if multiple positions have equal
            reward. May return an empty list of no valid positions
        """
    try:
        return [x[0] for x in value.items() if x[1] == max(rem_invalid(dict2list(value)))]
    except ValueError:
        return []
