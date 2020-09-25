# This code uses Astropy package to match catalogs from SExtractor outputs.

# Importing numpy and plot functions
from matplotlib import pyplot as plt 

# Importing Astropy packages
from astropy import units as u
from astropy import table
from astropy.coordinates import SkyCoord, match_coordinates_sky
from astropy.table import Table, vstack
from astropy.io import ascii
import numpy as np

directory = "/home/augusto/" # Working directory
img_name = "MOSAIC_g.fits" # FITS file
seo1 = "def.cat" # SExtractor Output 1
seo2 = "mex.cat" # SExtractor Output 2

# Importing the catalogs: cat_base is the base catalog whose objects we want to match
# [!] len(cat_base) > len(cat)

catA= Table.read('/home/augusto/def.cat',
                           format = 'ascii') # catalog we want to match
catB = Table.read('/home/augusto/mex.cat',
                           format = 'ascii') # base catalog

if len(catA) > len(catB):
    cat_base = catA
    cat = catB
else:
    cat_base = catB
    cat = catA

# Using SkyCoord to extract the ra and dec columns
cat1 = SkyCoord(ra=cat_base['ALPHA_J2000'], dec=cat_base['DELTA_J2000'],unit='deg') # gaussian filter
cat2 = SkyCoord(ra=cat['ALPHA_J2000'], dec=cat['DELTA_J2000'],unit='deg') # mexhat filter

# Matching the catalogs

#idx, sep, d3d = coord1.match_to_catalog_sky(coord2)

idx, sep, d3d = cat2.match_to_catalog_sky(cat1) # calculando cat1 intersec cat 2

# In the above line of code, idx are the indexes of the closest matches, sep is 
# the on-sky distance between the matches and d3d is the real-space distances
# between the matches

# Finding the matches

matches = cat1[idx]

# Getting the indexes of the matched objects to pass these into the original catalog

max_sep = 0.1*u.arcsec # Maximum separation constraint
idx1, sep1, d3d1 = match_coordinates_sky(matches[sep < max_sep], cat2, nthneighbor=1)

# Passing the indexes into the original catalog

cat_updated = table.unique(cat[idx1],keys='NUMBER') # This catalog contains only the non-matches between cat and cat_base

# Merging cat_updated and cat_base

final_catalog = vstack([cat_base, cat_updated])
final_catalog['NUMBER']=np.arange(1,len(final_catalog)+1) # rearranging the id of the items

#print(str('The number of objects in the final catalog is'))
print(len(final_catalog))

# Writing the final catalog
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
