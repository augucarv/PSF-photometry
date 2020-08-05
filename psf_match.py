# This code uses Astropy package to match hand-picked source positions for PSF
# to SExtractor outputs.

# Importing Astropy packages
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord, match_coordinates_sky
from astropy.table import Table
from astropy.io import ascii

# Fetching data

catA = Table.read('/home/augusto/GMOS_i_final.txt', format = 'ascii') # SExtractor output
catB = Table.read('/home/augusto/PSF_pos.reg', format = 'ascii') # PSF positions

# Converting the PSF positions from pixels to rad,dec

w = WCS('/home/augusto/NGC1600_GMOSS_i.sub.fits') # Getting the WCS info from main file
ra,dec = w.all_pix2world(catB[0][:],catB[1][:],1)

# Using SkyCoord to extract the ra and dec columns
coordA = SkyCoord(ra=catA['ALPHA_J2000'], dec=catA['DELTA_J2000'],unit='deg')
coordB = SkyCoord(ra, dec,unit='deg') 

# Matching the catalogs

#idx, sep, d3d = coord1.match_to_catalog_sky(coord2)
idx, sep, d3d = match_coordinates_sky(coordB, coordA, nthneighbor=1)

psf_match_cat = catA[idx]

# Writing the final catalog

ascii.write(psf_match_cat, 'psf_match_cat.txt', overwrite=True)

# Writing the final catalog as a .reg file to import to DS9

ascii.write(psf_match_cat['X_IMAGE_DBL','Y_IMAGE_DBL'], 'psf_match_cat.reg', overwrite=True)
