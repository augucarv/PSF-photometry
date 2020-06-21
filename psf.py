# This code uses the output of match_py and performs PSF photometry
# by using photutils's DAOPhotPSFPhotometry.

# Preping the data

import matplotlib.pyplot as plt
import numpy as np

from astropy.table import Table
from astropy.io import fits

# Importing the catalog from match_py

catalog = Table.read('YOUR_CATALOG.txt',
                           format = 'ascii')

# Importing data from the image

hdu_list = fits.open('YOUR_IMAGE.fits')
image_data = hdu_list[0].data

#plt.figure()
#plt.imshow(data, cmap='hot', vmin=0, vmax=10, interpolation='None', origin='lower')
#plt.plot(x_0, y_0, marker="o", markerfacecolor='None', markeredgecolor='y', linestyle='None')
#plt.colorbar(orientation='horizontal')

# Performing photometry

from photutils.psf import BasicPSFPhotometry
from photutils.psf import DAOGroup 
from photutils.psf import IntegratedGaussianPRF
from photutils.background import MMMBackground
from photutils.background import MADStdBackgroundRMS
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.stats import gaussian_sigma_to_fwhm

sigma_psf = 3.0
bkgrms = MADStdBackgroundRMS()
std = bkgrms(image_data)
daogroup = DAOGroup(2.0*sigma_psf*gaussian_sigma_to_fwhm)
mmm_bkg = MMMBackground()
psf_model = IntegratedGaussianPRF(sigma=sigma_psf)
fitter = LevMarLSQFitter()

psf_model.x_0.fixed = True
psf_model.y_0.fixed = True
positions = catalog['X_IMAGE_DBL', 'Y_IMAGE_DBL','FLUX_APER']
positions['X_IMAGE_DBL'].name = 'x_0'
positions['Y_IMAGE_DBL'].name = 'y_0'
positions['FLUX_APER'].name = 'flux_0'


photometry = BasicPSFPhotometry(group_maker=daogroup,
                                bkg_estimator=mmm_bkg,
                                psf_model=psf_model,
                                fitter=LevMarLSQFitter(),
                                fitshape=(11,11))

import timeit
tic=timeit.default_timer()

phot_results = photometry(image=image_data,init_guesses = positions)
residual = photometry.get_residual_image()
    
toc=timeit.default_timer()
print((toc-tic)/60)

# Writing the results
from astropy.io import ascii
ascii.write(phot_results, 'phot_results.txt', overwrite=True)
ascii.write(residual, 'residual.txt', overwrite=True)
##############################################################################
