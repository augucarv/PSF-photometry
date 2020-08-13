# This code merges 'match_cat.py' and 'psf_match.py'

# Importing Astropy packages
from astropy import units as u
from astropy import table
from astropy.coordinates import SkyCoord, match_coordinates_sky
from astropy.table import Table, vstack
from astropy.io import ascii
from astropy.wcs import WCS

# Defining the name of the .FITS file that will be worked with

# INPUTS

directory = "/home/augusto/NGC1600/" # Working directory
name = "GMOSS_i.fits" # FITS file
seo1 = name[:-5]+"_gauss_5.0_9x9.txt" # SExtractor Output 1
seo2 = name[:-5]+"_mexhat_5.0_11x11.txt" # SExtractor Output 2

# OUTPUTS

output_name = name[:-5]

# Importing the catalogs: cat_base is the base catalog whose objects we want to match
# [!] len(cat_base) > len(cat)

catA = Table.read(directory+seo1, format = 'ascii') # catalog we want to match
catB = Table.read(directory+seo2, format = 'ascii') # base catalog

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

idx, sep, d3d = match_coordinates_sky(cat2, cat1, nthneighbor=1)
matches = cat1[idx]

# Getting the indexes of the matched objects to pass these into the original catalog

max_sep = 0.1*u.arcsec # Maximum separation constraint
idx1, sep1, d3d1 = match_coordinates_sky(matches[sep > max_sep], cat2, nthneighbor=1)

# Passing the indexes into the original catalog

cat_updated = table.unique(cat[idx1],keys='NUMBER') # This catalog contains only the non-matches between cat and cat_base
print(str('The number of objects in cat that are not in cat_base is'))
print(len(cat_updated))

print(str('The first 5 items of the updated catalog are'))
print(cat_updated[:5])

# Merging cat_updated and cat_base

final_catalog = vstack([cat_base, cat_updated])

print(str('The number of objects in the final catalog is'))
print(len(final_catalog))

# Writing the final catalog

ascii.write(final_catalog, directory+output_name+"_final.txt", overwrite=True)

# Writing the final catalog as a .reg file to import to DS9

ascii.write(final_catalog['X_IMAGE_DBL','Y_IMAGE_DBL'], directory+output_name+"_final.reg", overwrite=True)

# Writing the final catalog as a .coo as input to DAOPHOT

ascii.write(final_catalog['NUMBER','X_IMAGE_DBL','Y_IMAGE_DBL'], directory+output_name+".coo", overwrite=True)

# PSF match ###################################################################

# This code uses Astropy package to match hand-picked source positions for PSF
# to SExtractor outputs.

# Fetching data

catA = Table.read(directory+output_name+"_final.txt", format = 'ascii') # SExtractor output
catB = Table.read(directory+"PSF_pos.reg", format = 'ascii') # PSF positions

# Converting the PSF positions from pixels to rad,dec

w = WCS(directory+name) # Getting the WCS info from main file
ra,dec = w.all_pix2world(catB[0][:],catB[1][:],1)

# Using SkyCoord to extract the ra and dec columns
coordA = SkyCoord(ra=catA['ALPHA_J2000'], dec=catA['DELTA_J2000'],unit='deg')
coordB = SkyCoord(ra, dec,unit='deg') 

# Matching the catalogs

#idx, sep, d3d = coord1.match_to_catalog_sky(coord2)
idx, sep, d3d = match_coordinates_sky(coordB, coordA, nthneighbor=1)

psf_match_cat = catA[idx]

# Writing the final catalog

ascii.write(psf_match_cat, directory+output_name+"_PSF_final.txt", overwrite=True)

# Writing the final catalog as a .reg file to import to DS9

ascii.write(psf_match_cat['X_IMAGE_DBL','Y_IMAGE_DBL'], directory+output_name+"_PSF_final.reg", overwrite=True)

# Writing the final catalog as a .lst as input to DAOPHOT

ascii.write(psf_match_cat['NUMBER','X_IMAGE_DBL','Y_IMAGE_DBL'], directory+output_name+".lst", overwrite=True)