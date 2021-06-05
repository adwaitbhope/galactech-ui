import base64
from model.regressors import AgeRegressor
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
        self.regressor = AgeRegressor()
        print('Pipeline ready')

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
        ages, metallicities = self.regressor.predict(X)

        ages, metallicities = self._prettify_results(entities, ages, metallicities)

        predictions = {}
        predictions['entity'] = entities
        predictions['age'] = ages
        predictions['metallicity'] = metallicities

        dataframe, csv = self._get_dataframe(filenames, predictions)

        return predictions, dataframe, csv

    def _prepare_data(self, wavelength, flux):
        X = resample(wavelength, flux)
        return X

    def _prettify_results(self, entities, ages, metallicities):
        for i, values in enumerate(zip(entities, ages, metallicities)):
            entity, age, metallicity = values

            age = (10 ** age) / 10 ** 9
            if age < 1:
                age = f'{int(age * 1000)} million years'
            else:
                age = f'{age:.2f} billion years'

            metallicity = f'{metallicity:.2f}'

            if entity != 'Galaxy':
                age = '-'
                metallicity = '-'

            ages[i] = age
            metallicities[i] = metallicity

        return ages, metallicities

    def _get_dataframe(self, filenames, predictions):
        dataframe = pd.DataFrame()
        dataframe['File'] = filenames
        dataframe['Entity'] = predictions['entity']
        dataframe['Age'] = predictions['age']
        dataframe['Metallicity'] = predictions['metallicity']

        csv = dataframe.to_csv(index=False).encode()

        return dataframe, base64.b64encode(csv).decode()
