# Introduction

This repository contains codes and tutorials useful for astrophysics and astronomy scientific research. 

# Contents

1. ```PyRAF_Install_Ubuntu.md``` contains instructions on how to install IRAF/PyRAF on Ubuntu 20.04 LTS
2. ```match_cat.py``` cross-matches two catalogs from SEXtractor outputs. Both catalogs are from the same image processed in SExtractor with different filters. The file returns a final catalog with all the sources and a .reg file to be used with DS9
3. ```psf.py``` performs PSF photometry in an astronomical FITS image (which is the output from "match_cat.py") and returns the residual one, by using the Astropy package. This feature in the package still is experimental and NOT recommended for uses whose aims are research results/publications. For this, use the stand-alone version (see item 5).
4. ```plot.py``` plots the original image and the residual one obtained from "psf.py" (this now also embedded in the "psf.py" file)
5. The folder DAOPHOT contains instructions on how to install the stand-alone version of DAOPHOT II, a software publisher by Stetson (1987) for performing photometry tasks in astronomical images. The reference paper is

Stetson, P. B. (1987). DAOPHOT: A computer program for crowded-field stellar photometry. Publications of the Astronomical Society of the Pacific, 99(613), 191.
