from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import numpy as np

testing = False


class NeuralNet:
    def __init__(self, layer_params, input_neurons, _input_shape=(9,), _activation='relu'):
        self.model = Sequential()
        self.layer_params = layer_params
        self.gamma = 0.1

        self.model.add(Dense(input_neurons, input_shape=_input_shape, activation='relu'))
        for layer in self.layer_params:
            self.model.add(Dense(layer[0], activation=layer[1]))
            self.model.compile(loss='mean_squared_error', optimizer=SGD(lr=0.1))

    def get_value_of_board_q_learning(self, board):
        val = self.model.predict_proba(np.matrix.flatten(board.board).reshape(1, 9))
        idx = 0
        val_dict = {}

        for i in range(board.rows):
            for j in range(board.cols):
                val_dict[(i, j)] = val[0][idx]
                idx += 1
        for key in val_dict.keys():
            val_dict[key] = -np.inf if not board.check_if_valid(key) else val_dict[key]
        #print(val_dict)
        return val_dict


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

        model.fit(inputs, outputs, batch_size=1, epochs=100)
        print(model.predict_proba(np.array([[0, 0]]))[0][0])
