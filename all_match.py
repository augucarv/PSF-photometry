# This code uses Astropy package to match catalogs from SExtractor outputs.

# Importing Astropy packages
from astropy.table import Table, vstack
from astropy.io import ascii
import numpy as np
from scipy.spatial.distance import cdist

# Importing the catalogs: cat_base is the base catalog whose objects we want to match
# [!] len(cat_base) > len(cat)

directory = "WORK_DIR" # Working directory
img_name = "IMG_NAME.fits" # FITS file
seo1 = "FILTER1_OUT.cat" # SExtractor Output 1
seo2 = "FILTER2_OUT.cat" # SExtractor Output 2

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

lim = 1000
n_batches = round(len(A)/lim) # Number of batches

sep = 3 # Maximum distance separation criterion [pixels]

dist = []
idx = []
idx_matches = []

for i in range(0,n_batches+1):
    bottom_lim = i*lim
    upper_lim = min(lim+i*lim-1,len(A))
    dist = cdist(A[bottom_lim:upper_lim], B, metric='euclidean')
    idx = np.argmin(dist > sep, axis=1)
    idx2 = idx[idx>0]
    idx_matches = np.append(idx_matches,idx2)
    dist = []
    idx = []

cat_base.remove_rows(idx_matches.astype(int)) # Removing the matches from B


# Appending catA to new catB to create the final catalog

final_catalog = vstack([cat_base,cat])
final_catalog['NUMBER']=np.arange(1,len(final_catalog)+1) # rearranging the id of the items

# Writing the final catalog as a .reg file to import to DS9

ascii.write(final_catalog, directory+img_name[:-5]+'.txt', overwrite=True)
ascii.write(final_catalog['NUMBER','X_IMAGE_DBL','Y_IMAGE_DBL'], directory+img_name[:-5]+'.coo', overwrite=True)
ascii.write(final_catalog['X_IMAGE_DBL','Y_IMAGE_DBL'],directory+'final.reg', overwrite=True) # check .reg file
