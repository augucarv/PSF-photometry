# This code uses the catalogs made with match_py and performs PSF photometry
# by using photutils's DAOPhotPSFPhotometry.

# Preping the data

import matplotlib.pyplot as plt
import numpy as np

from astropy.table import Table
from astropy.io import fits

# Importing the catalog from match_py

catalog = Table.read('/home/augusto/Pilot/Results/MOSAIC_g_final.txt',
                           format = 'ascii')

# Importing data from the image

hdu_list = fits.open('/home/augusto/Documentos/UFRGS/Pesquisa/subtracted/NGC1600_MOSAIC_g.sub.fits')
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
ascii.write(phot_results, 'phot_results_MOSAIC_g.txt', overwrite=True)
ascii.write(residual, 'residual_MOSAIC_g.txt', overwrite=True)
##############################################################################

#from photutils import DAOPhotPSFPhotometry
#from photutils.psf import IntegratedGaussianPRF
#from astropy.modeling.fitting import LevMarLSQFitter
#
#psf_model = IntegratedGaussianPRF(sigma=3.0)
#
#psf_model.x_0.fixed = True
#psf_model.y_0.fixed = True
#positions = catalog['X_IMAGE_DBL', 'Y_IMAGE_DBL','FLUX_APER']
#positions['X_IMAGE_DBL'].name = 'x_0'
#positions['Y_IMAGE_DBL'].name = 'y_0'
#positions['FLUX_APER'].name = 'flux_0'
#
#photometry = DAOPhotPSFPhotometry(crit_separation=3, 
#                                  threshold=3.0, 
#                                  fwhm=1, 
#                                  psf_model=psf_model, 
#                                  fitshape=(11,11), 
#                                  fitter=LevMarLSQFitter(), 
#                                  niters=3, 
#                                  aperture_radius=None)
#
#import timeit
#tic=timeit.default_timer()
#
#phot_results = photometry(image=image_data,init_guesses = positions)
#residual = photometry.get_residual_image()
#    
#toc=timeit.default_timer()
#(toc-tic)/60

#phot_results = Table.read('/home/augusto/phot_results.txt',
#                           format = 'ascii')
#
#plt.scatter(catalog['FLUX_APER'], phot_results['flux_unc'][0:len(catalog['FLUX_APER'])])
#plt.xlabel('Ground-truth fluxes')
#plt.ylabel('Estimated fluxes')
#plt.ylim((-1000,1000))


