# Introduction

This repository contains codes and tutorials useful for astrophysics and astronomy scientific research, with focus on PSF photometry.

# Contents

1. ```PyRAF_Install_Ubuntu.md``` contains instructions on how to install IRAF/PyRAF on Ubuntu 20.04 LTS
2. ```match_cat.py``` cross-matches two catalogs from SEXtractor outputs. Both catalogs are from the same image processed in SExtractor with different filters. The file returns a final catalog with all the sources and a .reg file to be used with DS9
3. ```psf.py``` performs PSF photometry in an astronomical FITS image (which is the output from "match_cat.py") and returns the residual one, by using the Astropy package. This feature in the package still is experimental and NOT recommended for uses whose aims are research results/publications. For this, use the stand-alone version (see item 5).
4. ```plot.py``` plots the original image and the residual one obtained from "psf.py" (this now also embedded in the "psf.py" file)
5. The folder DAOPHOT contains instructions on how to install the stand-alone version of DAOPHOT II, a software published by Stetson (1987) for performing photometry tasks in astronomical images. The reference paper is

Stetson, P. B. (1987). DAOPHOT: A computer program for crowded-field stellar photometry. Publications of the Astronomical Society of the Pacific, 99(613), 191.

6. On the file ```psf_match.py```: when you want to perform PSF photometry, you have to chose the sources that will be used to generate the PSF function. This choice is most useful done using PyRAF's ```imexamine``` alongside DS9. Since the sources have to be hand-picked, their coordinates not necessarily will *exactly* match the ones in the main catalog, as outputed by SExtractor. That being said, ```psf_match.py``` does this match for you and returns the "filtered" main catalog, which will be used as a .coo file when calling the ```PHOTOMETRY``` function in DAOPHOT.

To check the feasibility of each hand-picked source, run ```imexamine``` and open the original .fits file with DS9. Put the cursor above the source you believe is a good one and press ```r```. It will show the radial profile of the source, which should match the theoretical dashed curve, as in pictures below:

<p align="center">
<img class="gatsby-resp-image-image" src="https://github.com/augucarv/PSF-photometry/blob/master/images/psf1.png" width="500" height="300" />
</p>

<p align="center">
<img class="gatsby-resp-image-image" src="https://github.com/augucarv/PSF-photometry/blob/master/images/psf2.png" width="500" height="300" />
</p>

<p align="center">
<img class="gatsby-resp-image-image" src="https://github.com/augucarv/PSF-photometry/blob/master/images/psf3.png" width="500" height="300" />
</p>

The top picture is clearly not a good match. While the middle one might seem a good fit, when you check the bottom figure you'll perceive that a good fit is clearly distinguishable. 
