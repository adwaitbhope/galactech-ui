import base64
import numpy as np
import pandas as pd
from .classifiers import EntityClassifier
from model.data_transformations import resample


class Pipeline:
    '''
    This class serves as a wrapper for interacting with the ML model
    '''
    __pipeline = None

    @staticmethod
    def initialize():
        if not Pipeline.__pipeline:
            Pipeline.__pipeline = Pipeline()
        return Pipeline.__pipeline

    def __init__(self):
        # Initialize model as a class variable
        # Following line will be replaced by an actual instantiation of a model
        # Using some particular ML library
        print('Initializing pipeline...')
        self.entity_classifier = EntityClassifier()

    def process(self, filenames, spectra):
        '''
        Parameters:
            spectra: A list of dictinaries with wavelength and flux

        Returns:
            predictions: A list of dictionaries object with key-value pairs like age, metallicity, etc.
        '''

        X = [self._prepare_data(spectrum['wavelength'], spectrum['flux']) for spectrum in spectra]
        X = np.array(X)

        # Run the model over the input data here
        entities = self.entity_classifier.predict(X)

        predictions = {}
        predictions['entity'] = entities
        predictions['age'] = ['500 million years'] * len(X)
        predictions['metallicity'] = ['0.59'] * len(X)

        dataframe, csv = self._get_dataframe(filenames, predictions)

        return predictions, dataframe, csv

    def _prepare_data(self, wavelength, flux):
        X = resample(wavelength, flux)
        return X

    def _get_dataframe(self, filenames, predictions):
        dataframe = pd.DataFrame()
        dataframe['File'] = filenames
        dataframe['Entity'] = predictions['entity']
        dataframe['Age'] = predictions['age']
        dataframe['Metallicity'] = predictions['metallicity']

        csv = dataframe.to_csv(index=False).encode()

        return dataframe, base64.b64encode(csv).decode()
