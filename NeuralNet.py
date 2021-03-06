from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import SGD, Adam
import numpy as np
from Board import print_board

testing = True


class NeuralNet:
    def __init__(self, layer_params, input_neurons, load_net_from_file, _input_shape=(9,), _activation='relu'):
        self.model = Sequential()
        self.layer_params = layer_params
        self.gamma = 0.01
        if not load_net_from_file:
            self.model.add(Dense(input_neurons, input_shape=_input_shape, activation='relu'))
            for layer in self.layer_params:
                self.model.add(Dense(layer[0], activation=layer[1]))
                self.model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.05))
        else:
            self.load_net()

    def get_value_of_board_q_learning(self, next_boards):
        """Approximates the q-value of every possible move given the current state of the board. It works by computing
            the q-value of each of the next possible boards that are 1 move away.
            A more optimal way to do this is to have the neural net return the q value for each action. The problem is
            that I don't know how to update the weights of the neural net if I don't have a target value for each
            q-value for each action. (DeepMind did it this way..)

            # Arguments
                next_boards: a dict of all of the next possible boards that are 1 move away where keys are the action

            # Returns
                a dictionary that links actions to q-values
        """
        q_val = {}
        for a in next_boards.keys():
            # Set the (predicted) q-value
            q_val[a] = self.model.predict_proba(np.matrix.flatten(next_boards[a].board).reshape(1, 9))[0][0]

        return q_val

    def train_network(self, game_memory, batch_size=100):
        # Calculate reward given a current state
        if batch_size > len(game_memory):
            batch_size = len(game_memory)
        for i in range(batch_size):
            #episode = np.random.choice(game_memory)
            episode = game_memory[0]
            step = np.random.randint(0, len(episode.action))

            '''
                        print("Player: %d" % episode.player)
                        for b in episode.boards:
                            print_board(b)
                            print("\n")
                        print("Actions: " + str(episode.action))
                        for q in episode.q_values:
                            print("\t"+str(q))
                        print("Len q values: %d" % len(episode.q_values))
                        print("Reward: " + str(episode.reward))
                        print("Player won: %d" % episode.player_won)
                        print("Step: %d" % step)
                        print("\tAction: " + str(episode.action[step]))
                        print("\tReward: %d" % episode.reward[step])
                        print("\tQ-value: %d" % episode.q_values[step][episode.action[step]])
            '''
            target = self.calculate_target(episode, step)
            x = prepare_input(episode, step)
            target = np.array([[target]])

            print("\tTarget: " + str(target))
            print_board(episode.boards[step])
            print("\n")
            self.model.fit(x, target, batch_size=1, epochs=5, verbose=0)

            # input()

            #if target > 0:
            #    print(episode.q_values[step][episode.action[step]])
            #    print(target)
            #    print("\n")


            game_memory.remove(episode)

        '''
        print("Reward: " + str(game_memory[0].reward[idx]))
        print("Action: " + str(game_memory[0].action[idx]))
        print("Q_Value: " + str(game_memory[0].q_values[idx][game_memory[0].action[idx]]))
        print("Target: " + str(target))
        input()
        '''

    def calculate_target(self, episode, index):
        if index == len(episode.action)-1:
            return episode.reward[index]
        else:
            target = 0
            for i in range(index, len(episode.q_values)):
                target += (self.gamma**(i-index))*(max(episode.q_values[i].values()))
            return target


    def save_net(self):
        self.model.save("saved_neural_net")

    def load_net(self):
        try:
            self.model = load_model("saved_neural_net")
        except OSError:
            print("Unable to open file!")
            exit(0)


def prepare_input(episode, index):
    if episode.boards[index][episode.action[index]] != 0:
        print_board(episode.boards[index])
        exit(0)
    episode.boards[index][episode.action[index]] = episode.player
    return np.matrix.flatten(episode.boards[index]).reshape(1, 9)

if __name__ == '__main__':
    if not testing:
        pass
    if testing:
        model = Sequential()
        model.add(Dense(8, input_shape=(2,), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        sgd = SGD(lr=0.1)
        model.compile(loss='mean_squared_error', optimizer=sgd)
        inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        outputs = np.array([[0], [1], [1], [0]])
        print(inputs.shape)
        print(outputs.shape)
        model.fit(inputs, outputs, batch_size=1, epochs=100)
        print(model.predict_proba(np.array([[0, 0]]))[0][0])
