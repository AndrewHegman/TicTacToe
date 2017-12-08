from Agent import Agent
from Board import GameBoard


def convert_to_position(pos, rows, cols):
    return [int(pos / rows), pos % cols]


def play_game(players):
    board = GameBoard()
    board.board[0][0] = 1
    player = 0
    player_won = 0
    while player_won == 0:
        if any([x.is_human for x in players]):
            board.show_board()
        if players[player].is_human:
            requested_pos = convert_to_position(players[player].request_move(), board.rows, board.cols)
            while not board.check_if_valid(requested_pos):
                requested_pos = convert_to_position(players[player].request_move(), board.rows, board.cols)
        else:
            pass
            #players[player].get_move()
        board.board[requested_pos[0], requested_pos[1]] = players[player].number
        player = 1 if player == 0 else 0
        player_won = board.check_for_win()

    if any([x.is_human for x in players]):
        board.show_board()

    return player_won


def main():
    player1 = Agent(1, True)
    play_game((player1, player1))

main()