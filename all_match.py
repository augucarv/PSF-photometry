# This code merges 'match_cat.py' and 'psf_match.py'

# This code uses Astropy package to match catalogs from SExtractor outputs.

# Importing Astropy packages
from astropy.table import Table, vstack
from astropy.io import ascii
import numpy as np
from scipy.spatial.distance import cdist

# Importing the catalogs: cat_base is the base catalog whose objects we want to match
# [!] len(cat_base) > len(cat)

directory = "[WORK_DIR]" # Working directory
img_name = "[FILE_NAME].fits" # FITS file
seo1 = "def.cat" # SExtractor Output 1
seo2 = "mex.cat" # SExtractor Output 2

catA = Table.read(directory+seo1, format = 'ascii')
catB = Table.read(directory+seo2,format = 'ascii') 

if len(catA) > len(catB):
    cat_base = catA
    cat = catB
else:
    cat_base = catB
    cat = catA

# Matching the catalogs

A = np.array([cat['X_IMAGE_DBL'],cat['Y_IMAGE_DBL']]).T
B = np.array([cat_base['X_IMAGE_DBL'],cat_base['Y_IMAGE_DBL']]).T
dist = cdist(A, B)
idx = np.argmin(dist > 3, axis=1)
idx2 = idx[idx>0]
matches = B[idx2, :] # checking the matches
cat_base.remove_rows(idx2) # Removing the matches from B

# Appending catA to new catB to create the final catalog

final_catalog = vstack([cat_base,cat])
final_catalog['NUMBER']=np.arange(1,len(final_catalog)+1) # rearranging the id of the items

# Writing the final catalog as a .reg file to import to DS9

ascii.write(final_catalog, directory+img_name[:-5]+'.txt', overwrite=True)
ascii.write(final_catalog['NUMBER','X_IMAGE_DBL','Y_IMAGE_DBL'], directory+img_name[:-5]+'.coo', overwrite=True)
ascii.write(final_catalog['X_IMAGE_DBL','Y_IMAGE_DBL'],directory+'final.reg', overwrite=True) # check .reg file

########## .lst file #########################################################

from astropy.wcs import WCS
from astropy.coordinates import SkyCoord, match_coordinates_sky

catalog_name = directory+img_name[:-5]+'.txt'
psf_name = 'PSF_pos.reg'

# Fetching data

catC = Table.read(catalog_name, format = 'ascii') # SExtractor output
catD = Table.read(directory+psf_name, format = 'ascii') # PSF positions

# Converting the PSF positions from pixels to rad,dec

w = WCS(directory+img_name) # Getting the WCS info from main file
ra,dec = w.all_pix2world(catD[0][:],catD[1][:],1)

# Using SkyCoord to extract the ra and dec columns
coordA = SkyCoord(ra=catC['ALPHA_J2000'], dec=catC['DELTA_J2000'],unit='deg')
coordB = SkyCoord(ra, dec,unit='deg') 

# Matching the catalogs

#idx, sep, d3d = coord1.match_to_catalog_sky(coord2)
idx, sep, d3d = match_coordinates_sky(coordB, coordA, nthneighbor=1)

psf_match_cat = catC[idx]

# Writing the final catalog as a .lst for DAOPHOT

ascii.write(psf_match_cat['NUMBER','X_IMAGE_DBL','Y_IMAGE_DBL'], directory+img_name[:-5]+'.lst', overwrite=True)
