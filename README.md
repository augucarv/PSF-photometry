# Introduction

This repository contains codes and tutorials useful for astrophysics and astronomy scientific research, with focus on PSF photometry.

# Contents

1. ```PyRAF_Install_Ubuntu.md``` contains instructions on how to install IRAF/PyRAF on Ubuntu 20.04 LTS
2. ```match_cat.py``` cross-matches two catalogs from SEXtractor outputs. Both catalogs are from the same image processed in SExtractor with different filters. The file returns a final catalog with all the sources and a .reg file to be used with DS9
3. ```psf.py``` performs PSF photometry in an astronomical FITS image (which is the output from "match_cat.py") and returns the residual one, by using the Astropy package. This feature in the package still is experimental and NOT recommended for uses whose aims are research results/publications. For this, use the stand-alone version (see item 5).
4. ```plot.py``` plots the original image and the residual one obtained from "psf.py" (this now also embedded in the "psf.py" file)
5. The folder DAOPHOT contains instructions on how to install and configure the stand-alone version of DAOPHOT II, a software published by Stetson (1987) for performing photometry tasks in astronomical images. You need to contact him directly to get access to the software. The reference paper is:  Stetson, P. B. (1987). *DAOPHOT: A computer program for crowded-field stellar photometry. Publications of the Astronomical Society of the Pacific*, 99(613), 191.

6. The file ```psf_match.py``` matches your hand-picked sources from DS9 to the output catalog from ```source-extractor```.

7. The file ```all_match.py``` combines ```match_cat.py``` and ```psf_match.py```  in a single script.

# PSF photometry: Step-by-step

This guide considers that you have already have [installed SExtractor](https://www.astromatic.net/software/sextractor) and [DAOPHOT](http://www.star.bris.ac.uk/~mbt/daophot/).

1. Run ```source-extractor``` in the .fits file you want to assess. Include the name of the filter you use at the end of the file's name, e.g. if your file is "my_file.fits" and the filter you use is "filterX.conv", the output catalog from ```source-extractor``` would be "my_file_filterX.txt".

2. Run ```source-extractor``` again, this time with a different filter and name it as in step 1. Hint: the filters in the ```source-extractor``` folder start with the name of the filter, e.g. mexhat, gauss etc., followed by a float number, e.g. 1.5, 2.0, 5.0, which represents the FWHM used in the filter. This should be as close as possible to the FWHM of your .fits file. The other number in the filter's name, e.g. 4x4, 5x5, 9x9 etc. represents the window to be used during the convolution.

3. Pick the sources for the psf. You can do this by using PyRAF/IRAF's ```imexamine``` command alongside DS9. To do so: (1) Open DS9; (2) go to the "Edit" tab and select "Region", (3) open the terminal and start either IRAF or PyRAF, whatever suits you; (4) run ```imexamine``` , addressing it to the original .fits file. With the file open, put the cursor above the source you believe is a good candidate and press ```r```. It will show its radial profile, which should match the theoretical dashed curve, as in the images below. If the plot shown when you press ```r``` is similar to the third picture, then left-click with the mouse and it should now be selected, with a green region in its surroundings. Do the same for as many sources as you wish to have. The higher this number, the better. After you finish this process, go to the tab "Regions" and save the region as ```PSF_pos.reg```. 

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

4. So far you have generated three files: the two catalogs from ```source-extractor``` and the ```PSF_pos.reg``` from DS9. Now you need to: (1) cross-match the two outputs from ```source-extractor``` and generate a single catalog from those and (2) map your hand-picked sources from ```PSF_pos.reg``` to this newly-generated catalog. To do so, run either ```all_match.py``` or ```match_cat.py``` + ```psf_match.py```. The first option (```all_match.py```) is handier and is just a merge of the last two, but you're welcome to play around with all of them. Your main outputs here are the .coo and the .lst file, which will be used as inputs to DAOPHOT.

5. Run ```daophot``` and ```attach``` your image. Then use ```find``` to generate a .coo file. Name it diffrentely than the one generated with ```all_match.py```. This step is needed because you need to replace the header in the first .coo file. The header of this latter one is 

```
NUMBER X_IMAGE_DBL Y_IMAGE_DBL
```

The header of the one generated with ```find``` is something like

``` 
NL    NX    NY  LOWBAD HIGHBAD  THRESH     AP1  PH/ADU  RNOISE    FRAD
  1  3414  2350  -442.1 42000.0   5.740   0.000   4.000   4.455   3.200
 
```

Simply copy-and-paste and replace the former with the latter. Do the same for the .lst file. For this one, you use the same header as for the .coo, but the number below the NL column is 3 rather than 1. So, for the .lst file, the header will change from 

```
NUMBER X_IMAGE_DBL Y_IMAGE_DBL
```

to

``` 
NL    NX    NY  LOWBAD HIGHBAD  THRESH     AP1  PH/ADU  RNOISE    FRAD
  3  3414  2350  -442.1 42000.0   5.740   0.000   4.000   4.455   3.200
 
```

I've not have time to automate this yet, but be welcome to do so and let me know! :)

6. You can now finally run ```daophot``` for real. Attach the original image and use the .coo as input. Run ```photometry```. You'll be given a .ap file.

7. Run ```psf``` and use the .lst as input. This latter has the coordinates of the sources used to perform the psf. Remember you've hand-picked these and matched this output with the output from ```source-extractor``` to find the right positions. Just a reminder :)

Now, when you run ```psf```, you will be given the Profile errors in the terminal: 

``` 
Profile errors:

  10444  0.592      8774  0.077     11551  0.698     16729  0.138      7316  0.862   
   9453  0.465      5585  1.016      9544  1.284 ?   17631  0.056      4265  0.821   
  15543  1.127      7319 defective  10884  0.082     17496  0.718      2595  0.687   
  20310  1.369 ?   14676  0.897     12165  0.084     18087  0.923      8096  0.576   
  16946  0.236     13258  0.723     19457  0.144     19820  0.519      6525  0.827   
   4435  1.269 ?   17379  1.130      7695  0.279     20408  0.210     16591  0.614   
   4394  0.202     17628  5.987 *    8055  0.221     13300  0.158     11459  0.467   
   4441  0.148     13408  0.910     13930  0.354     12493  0.653     18647  0.095   
   8143  1.296 ?   11601  0.339     15016  0.206     12539  0.727      6127  0.644 
```
Some will be marked with a question mark, others as defective, others with an asterisk. You want to remove these, since, as you can see, their errors are way too big in comparison to the others'. Manually open your .lst file and remove this instances. Then run ```psf``` again and again until no markers appear in the Profile errors output. After a few runs, this output should look like:

```
 Profile errors:

  10444  0.590     13258  0.713      8055  0.240     20408  0.222      6525  0.823   
   9453  0.474     13408  0.896     13930  0.351     13300  0.160     16591  0.578   
  16946  0.251     11601  0.344     15016  0.211     12493  0.689     11459  0.459   
   4394  0.197     11551  0.691     16729  0.152     12539  0.711     18647  0.094   
   4441  0.149     10884  0.081     17631  0.043      7316  0.888      6127  0.631   
   8774  0.086     12165  0.096     17496  0.713      4265  0.814                    
   5585  0.963     19457  0.158     18087  0.940      2595  0.678                    
  14676  0.882      7695  0.268     19820  0.523      8096  0.575 
```

As you can see, the errors are somewhat big. This is because not enough sources were selected. As you select more sources, these values should get smaller and smaller, so make sure you pick at least 50 points, knowing that the more you have, the better your final results will be.

7. Now you can ```exit``` DAOPHOT and run ```allstar```, which will generate the residual image for you. Attach the original .fits file and keep attaching the files as the terminal requests them. Generally you only need to keep pressing ```ENTER``` until the terminal stops asking you for inputs. It might take some time calculating things but at the end it should return the residual image and you're done with subtraction for now. :)

8. After having the residual image, it's time to plot the color-magnitude diagram (CMD) and GCLF (in the case of globular clusters). For that, run `daomatch` and input both `.als` files the you got from `daophot`, one for each filter. Run `daomatch` and, after that, `daomaster`, following instructions on the screen. After that, use `cmdmaker.py` on your `.raw` file that you got from running `daomaster`. If you're in doubt on how to do that, just follow David Hogg's [guide](www.astro.uvic.ca/~yang/a329/intro/imaging_proc.html).
