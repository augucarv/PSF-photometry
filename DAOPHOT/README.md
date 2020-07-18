# Instructions

Make sure you have IRAF installed in your system. Check how to this in the PyRAF_Install_Ubuntu.md file of this repository.

1. Install gfortran, which is the compiler used for DAOPHOT II routines:

> ```$ sudo apt-get install gfortran```

2. Install gfortran-multilib, since you're running a 32-bits code in a 64-bits system:

> ```$ sudo apt-get install gfortran-multilib```

3. Install the libcfitsio-dev library:

> ```$ sudo apt-get install libcfitsio-dev```

4. In the original Makerfile.linux, you have to change the following lines from

```
F77 = g77
FFLAGS = -c -O2
LFLAGS = -O2 -Wall -Wsurprising --defsym,mem_=0 -fbounds-check
```
to

```
F77 = gfortran
FFLAGS = -c -O2 -m32
LFLAGS = -O2 -Wall -m32
```

The -m32 instance runs the code as in a 32-bits system, and removing the 
```-Wsurprising --defsym,mem_=0 -fbounds-check``` prevents an error in the next step.

5. Run the command ```$ make daophot```.

You should now have a binary file that is run by ```./daophot```. The prompt should return
```
Value unacceptable --- please re-enter

                        READ NOISE (ADU; 1 frame) = 
```
