from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import numpy as np

model = Sequential()
model.add(Dense(8, input_dim=2, activation='tanh'))
model.add(Dense(1, activation='sigmoid'))
#model.add(Dense(81, activation='relu'))
#model.add(Dense(9, activation='relu'))
sgd = SGD(lr=0.1)
model.compile(optimizer=SGD(lr=0.1), loss='mean_squared_error')
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([[0], [1], [1], [0]])

model.fit(x=inputs, y=outputs, epochs=1000)
print(model.predict(inputs, batch_size=1, verbose=1))
#board = np.zeros((1, 9))
#board[0][0] = 1
#print(model.predict(board, batch_size=1, verbose=1))
#model.save_weights('test_weights.h5')


