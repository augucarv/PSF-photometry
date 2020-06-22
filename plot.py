# This code plots the PSF results (residual image) against the original one

from astropy.io import fits
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
# Importing data from the image

hdu_list = fits.open('/home/augusto/Documentos/UFRGS/Pesquisa/subtracted/NGC1600_GMOSS_i.sub.fits')
image_data = hdu_list[0].data
residual = pd.read_table("/home/augusto/residual_GMOS_i.txt",sep="\s+")
# Plotting the images

fig = plt.figure()
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 
fig.suptitle("NGC1600 PSF (GMOSS, i-band)", fontsize=25)
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
