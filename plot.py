# This code plots the PSF results (residual image) against the original one

from astropy.io import fits
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
# Importing data from the image

hdu_list = fits.open('[FILE_DIRECTORY]') # Original file
image_data = hdu_list[0].data
residual = pd.read_table("[FILE_DIRECTORY]",sep="\s+") # Table containing the residual data, obtained from psf.py

# Plotting the images

fig = plt.figure()
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 
fig.suptitle("[TITLE]", fontsize=25)
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

# Writing the FITS file

hdu = fits.PrimaryHDU(residual)
hdulist = fits.HDUList([hdu])
hdulist.writeto('[FILE_NAME]')
