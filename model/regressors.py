import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten
from model.config import REGRESSION_MODEL


class AgeRegressor:

    def __init__(self):
        self._compile_model()
        self.model.load_weights(REGRESSION_MODEL)

    def _compile_model(self):
        self.model = Sequential()

        self.model.add(Conv1D(12, kernel_size=13, activation='relu', input_shape=(3000, 1), use_bias=True))
        self.model.add(MaxPooling1D(2))

        self.model.add(Conv1D(8, kernel_size=9, activation='relu', use_bias=True))
        self.model.add(MaxPooling1D(2))

        self.model.add(Conv1D(4, kernel_size=7, activation='relu', use_bias=True))
        self.model.add(MaxPooling1D(2))

        self.model.add(Flatten())
        self.model.add(Dense(8))
        self.model.add(Dense(2))

        self.model.compile(optimizer='adam', loss='mae')

    def predict(self, X):
        X = self._prepare_data(X)

        predictions = self.model.predict(X)
        ages, metallicites = list(predictions[:,0]), list(predictions[:,1])

        return ages, metallicites

    def _prepare_data(self, X):
        X = np.expand_dims(X[:,:3000], axis=-1)
        return X
