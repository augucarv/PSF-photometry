# This code uses the catalogs made with match_py and performs PSF photometry
# by using photutils's DAOPhotPSFPhotometry.
#
# INPUTS:  (1) Catalog obtained from match_cat.py
#          (2) FITS image of the region you want to evaluate
#          (3) Catalog or table with the sources chosen to create the PSF
# OUTPUTS: (1) Table with photometric results (fluxes)
#          (2) Table with data from the residual image
#          (3) The residual image itself

# Prepping the data

import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from astropy.io import fits

# Importing the catalog from match_cat.py

catalog = Table.read('/etc/YOUR_CATALOG.txt',
                           format = 'ascii')

x_0=catalog['X_IMAGE_DBL']
y_0=catalog['Y_IMAGE_DBL']
flux_0 = catalog['FLUX_APER']

# Importing data from the image

image_data = fits.getdata('/etc/YOUR_FITS_IMAGE.fits')

# Creating PRF from image data

psf_reg = Table.read('/etc/YOUR_PSF_SOURCES.reg',
                           format = 'ascii') # Importing the catalog of chosen sources

from photutils.psf.sandbox import DiscretePRF

mask = np.isfinite(image_data)

psf = DiscretePRF.create_from_image(image_data, 
                                    psf_reg, 
                                    size=15, 
                                    mask=np.logical_not(mask),
                                    mode='median', 
                                    subsampling=1) 

# Performing Photometry

psf.x_0.fixed = True
psf.y_0.fixed = True
pos = Table(names=['x_0', 'y_0'], data=[catalog['X_IMAGE_DBL'],catalog['Y_IMAGE_DBL']]) # Using the initial positions

from photutils.psf import DAOPhotPSFPhotometry

photometry=   DAOPhotPSFPhotometry(crit_separation=19, # The higher the crit_separation, the higher the computational cost
                                   threshold=1.0,
                                   fwhm=3.0,
                                   psf_model=psf,
                                   fitshape=9,
                                   sigma=3.0,
                                   ratio=1.0,
                                   theta=0.0,
                                   sigma_radius=1.5,
                                   sharplo=0.2,
                                   sharphi=1.0,
                                   roundlo=-1.0,
                                   roundhi=1.0,
                                   fitter=LevMarLSQFitter(),
                                   niters=3, 
                                   aperture_radius=5)

import timeit
tic=timeit.default_timer()

phot_results = photometry(image_data,init_guesses=pos)
residual = photometry.get_residual_image()

toc=timeit.default_timer()
print((toc-tic)/60)

# Plotting the images

import matplotlib 
from matplotlib.colors import LogNorm

fig = plt.figure()
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 
fig.suptitle("NGC1600 PSF (GMOS, i-band)", fontsize=25)
plt.subplot(1, 2, 1)
plt.imshow(image_data, cmap='gray_r', aspect=1,interpolation='nearest', origin='lower',norm=LogNorm())
plt.title('Image data',fontsize=22)
plt.xlabel('px', fontsize=20)
plt.ylabel('px', fontsize=20)
plt.colorbar(orientation='horizontal')
plt.subplot(1 ,2, 2)
plt.imshow(residual, cmap='gray_r', aspect=1,interpolation='nearest', origin='lower',norm=LogNorm())
plt.title('Residual Image',fontsize=22)
plt.xlabel('px', fontsize=20)
plt.ylabel('px', fontsize=20)
plt.colorbar(orientation='horizontal')

# Writing the results
from astropy.io import ascii
ascii.write(phot_results, 'phot_results.txt', overwrite=True)
ascii.write(residual, 'residual.txt', overwrite=True)

# Writing the FITS file of the residual image

hdu = fits.PrimaryHDU(residual)
hdulist = fits.HDUList([hdu])
hdulist.writeto('residual.fits',overwrite=True)
