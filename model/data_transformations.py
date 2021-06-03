import numpy as np
import pysynphot as S
from sklearn import preprocessing

Standardisation = preprocessing.StandardScaler()

wave_lower, wave_upper = 3850, 9150
wavelength_set = np.array([i for i in range(wave_lower, wave_upper + 1)])


def resample(wavelength, flux):
    sp = S.ArraySpectrum(wave=wavelength, flux=flux, waveunits='angstrom', fluxunits='photlam', keepneg=True)
    
    result = sp.resample(wavelength_set)
    
    return result.flux


def standardize(X):
    return Standardisation.fit_transform(X)
