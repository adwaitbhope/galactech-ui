import numpy as np
from joblib import load
from tensorflow.keras.models import model_from_yaml
from .config import ENTITY_CLASSIFIER_ARCH, ENTITY_CLASSIFIER_MODEL
# from .data_transformations import standardize

class EntityClassifier:

    def __init__(self):
        self.classes = ['Galaxy', 'Star', 'QSO']
        model_architecture = load(ENTITY_CLASSIFIER_ARCH)
        self.model = model_from_yaml(model_architecture)
        self.model.load_weights(ENTITY_CLASSIFIER_MODEL)

    def predict(self, X):
        X = self._prepare_data(X)

        predictions = self.model.predict(X)
        predictions = np.argmax(predictions, axis=1)

        return [self.classes[index] for index in predictions]

    def _prepare_data(self, X):
        X = np.expand_dims(X, axis=-1)
        return X
