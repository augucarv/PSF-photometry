PyRAF Installation Tutorial v1.0 - 20-03-2020
-----------------------------------------------------------------
This tutorial installs PyRAF on Debian-based Linux distributions (tested with Ubuntu 19.10)

1. Install the C libraries and X11 devtools needed*:

		$ sudo apt-get install libc6:i386 libz1:i386 libncurses5:i386 libbz2-1.0:i386 libuuid1:i386 libxcb1:i386

		$ sudo apt-get install libxmu-dev:i386

		$ sudo apt-get install libx11-dev

* Found on github here: https://github.com/astroconda/astroconda/issues/31#issuecomment-257404123
and on StackOverflow here: https://stackoverflow.com/questions/17911140/trouble-installing-python-package-group-stsci
-----------------------------------------------------------------
2. Install Anaconda or Miniconda (PyRAF recommends version with Python 2.7):

	2.1. Download the installer from https://docs.conda.io/en/latest/miniconda.html 

	2.2. Open terminal, change the directory to the download folder and run

		$ bash Miniconda2-latest-Linux-x86_64.sh

	2.3. Follow the instructions on the screen
-----------------------------------------------------------------
3. Install and setup PyRAF:

	3.1. Add the astroconda channel: 

		$ conda config --add channels http://ssb.stsci.edu/astroconda

	3.2. Create the environment where the PyRAF usage will take place:

		$ conda create -n NAME_OF_ENVIRONMENT python=2.7 iraf-all pyraf-all stsci

	3.3. Activate the environment:

		$ source activate NAME_OF_ENVIRONMENT

	3.4. Install and run PyRAF:

		$ pip install git+https://github.com/spacetelescope/pyraf.git@master
	
	3.5. Information from "Basic PyRAF", 2014 version by Matthew Bourque:

	'Ensure you have activated the conda environment that you set up in the Computer Setup
	section. Create a login.cl file to configure IRAF by running mkiraf in your home directory.
	When asked to Initialize uparm?, answer y. When prompted to Enter terminal
	type, you should supply xterm.'

	3.6. After the install, when typing pyraf in the terminal, the system should return something like:

		$ pyraf

		setting terminal type to xterm...

   		NOAO/IRAF PC-IRAF Revision 2.16 EXPORT Thu May 24 15:41:17 MST 2012
      		This is the EXPORT version of IRAF V2.16 supporting PC systems.


  		Welcome to IRAF.  To list the available commands, type ? or ??.  To get
  		detailed information about a command, type `help <command>'.  To run  a
  		command  or  load  a  package,  type  its name.   Type  `bye' to exit a
  		package, or `logout' to get out  of the CL.    Type `news' to find  out
  		what is new in the version of the system you are using.  

  		Visit http://iraf.net if you have questions or to report problems.

  		The following commands or packages are currently defined:

  		(Updated on 2013-12-13)


