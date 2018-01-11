from Agent import Agent
from Board import GameBoard
import numpy as np
from collections import namedtuple


"""game_memory uses a namedtuple:
    # arguments
        # boards
            a list of all boards, from perspective of player TWO
        # action
            action that player chooses
        # reward
            reward given to player TWO at each step
        # player_won
            which player won the game
                -1 = tie game
                1 = player 1 has won
                2 = player 2 has won
"""


def play_game(players, reward_for_winning=10, learning_player=2):
    """Plays a game given two players and saves board information for neural net training

            # Arguments
                players: a list of 2 agents. The agent at index 0 will always play first

            # Returns
                    A namedtuple representing memory (see above)
    """
    board = GameBoard()
    c_player = 0
    player_won = 0
    boards = []
    actions = []
    rewards = []
    mem = namedtuple("Memory", "boards action reward player_won")
    while player_won == 0:
        if players[c_player].is_human:
            board.show_board()
            print("\n")

        if players[c_player].number == learning_player:
            boards.append(np.copy(board.board))

        requested_pos = players[c_player].move(board)
        board.board[requested_pos[0], requested_pos[1]] = players[c_player].number

        if players[c_player].number == learning_player:
            actions.append(requested_pos)

        player_won = board.check_for_win()

        if players[c_player].number == learning_player:
            if player_won == learning_player:
                rewards.append(reward_for_winning)
            elif player_won == -1:
                rewards.append(reward_for_winning // 2)
            elif player_won == 0:
                rewards.append(0)
            else:
                rewards.append(-reward_for_winning)
        c_player = 1 if c_player == 0 else 0

    if any([x.is_human for x in players]):
        board.show_board()
        print("\n")

    boards.append(board.board)

    if rewards[-1] == 0:
        if player_won == learning_player:
            rewards[-1] = reward_for_winning
        elif player_won == -1:
            rewards[-1] = reward_for_winning // 2
        elif player_won == 0:
            rewards[-1] = 0
        else:
            rewards[-1] = -reward_for_winning

    mem.boards = boards
    mem.action = actions
    mem.player_won = player_won
    mem.reward = rewards
    return mem


def play_episode(first_player, second_player, learning_player, game_memory, games_per_episode, recursion):
    for i in range(games_per_episode):
        game_memory.append(play_game([first_player, second_player]))
    if recursion:
        return play_episode(second_player, first_player, learning_player, game_memory, games_per_episode, False)
    else:
        return game_memory





def check_win_percentage(game_memory):
    win_percentages = [0, 0, 0]
    for game in game_memory:
        print("Boards: %d" % len(game.boards))
        print("Action: " + str(game.action))
        print("Reward: " + str(game.reward))

        input()
        if game.player_won == -1:
            win_percentages[0] += 1
        elif game.player_won == 1:
            win_percentages[1] += 1
        elif game.player_won == 2:
            win_percentages[2] += 1
        else:
            raise Exception("I'm not even sure how this happened...")
    return win_percentages


if __name__ == '__main__':
    def main():
        print("What would you like to do: ")
        print("\t1. Start GUI")
        print("\t2. Train Neural Network")
        #choice = int(input("Type your choice: "))
        choice = 2
        if choice == 1:
            pass
        elif choice == 2:
            player1 = Agent(1, False, "minimax", depth=4)
            player2 = Agent(2, False, "q_learning")
            mem = []
            mem = play_episode(player1, player2, 2, mem, 10, True)
            win_percentages = check_win_percentage(mem)
            print("Player 1 has won %d%% of the games! (%d)" % (((win_percentages[1] / len(mem)) * 100), win_percentages[1]))
            print("Player 2 has won %d%% of the games! (%d)" % (((win_percentages[2] / len(mem)) * 100), win_percentages[2]))
            print("%d%% of the games have been ties! (%d)" % (((win_percentages[0] / len(mem)) * 100), win_percentages[0]))

    main()
