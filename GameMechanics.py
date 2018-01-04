from Agent import Agent, get_value_of_board, get_best_action
from Board import GameBoard, look_ahead


def play_game(players):
    board = GameBoard()
    c_player = 0
    player_won = 0

    while player_won == 0:
        if players[c_player].is_human:
            board.show_board()

        requested_pos = players[c_player].move(board)
        board.board[requested_pos[0], requested_pos[1]] = players[c_player].number
        c_player = 1 if c_player == 0 else 0
        player_won = board.check_for_win()

    if any([x.is_human for x in players]):
        board.show_board()

    return player_won


def main():
    player1 = Agent(1, True)
    player2 = Agent(2, False)
    play_game((player1, player2))

main()
