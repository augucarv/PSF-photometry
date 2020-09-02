# This code uses Astropy package to match sources of two catalogs from the same image with two different filters. 
# The catalogs are obtained by processing a FITS image on SExtractor.
#
# INPUTS: two catalogs from the same image with different filters
# OUTPUTS: a catalog in .txt format and a region file in .reg format to be imported in DS9

#-----------------------------------------------------------------------------------------------------------------------------

# Importing packages
from astropy.table import Table, vstack
from astropy.io import ascii
import numpy as np
from scipy.spatial.distance import cdist

# Importing the catalogs: cat_base is the base catalog whose objects we want to match
# [!] len(cat_base) > len(cat)

directory = "[WORK_DIR]" # Working directory
name = "[FILE_NAME].fits" # FITS file
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

ascii.write(final_catalog, directory+name[:-5]+'.coo', overwrite=True)
ascii.write(final_catalog['X_IMAGE_DBL','Y_IMAGE_DBL'],directory+'final.reg', overwrite=True)

