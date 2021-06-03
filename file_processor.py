import pandas as pd
from astropy.io import fits


def extract_spectra_from_files(files):
    spectra = []

    for file in files:
        # Check the file extension to appropriately extract spectral data
        if file.name.endswith('.csv') or file.name.endswith('.CSV'):
            wavelength, flux = get_spectra_from_csv(file)

        elif file.name.endswith('.fits') or file.name.endswith('.FITS'):
            wavelength, flux = get_spectra_from_fits(file)

        else:
            return None

        spectra.append({
            'wavelength': wavelength,
            'flux': flux
        })

    return spectra


def get_spectra_from_csv(file):
    '''
    Used to extract the spectra from a CSV file
    Returns:
        wavelength: A pandas Series object for Wavelength
        flux: A pandas Series object for Flux
    '''
    try:
        data = pd.read_csv(file)
        return data['Wavelength'], data['Flux']
    except:
        return [],[]


def get_spectra_from_fits(file):
    '''
    Used to extract the spectra from a FITS file
    Returns:
        wavelength: A pandas Series object for Wavelength
        flux: A pandas Series object for Flux
    '''
    try:
        hdul = fits.open(file)
        data = hdul[1].data

        # Extract Wavelength and invert the logarithm
        wavelength = 10 ** data['loglam']

        # Extract flux 
        flux = data['flux']
        
        # Create a pandas Series for Wavelength and Flux
        # wavelength = pd.Series(xdata)
        # flux = pd.Series(ydata)

        return wavelength, flux
    except:
        return [],[]
