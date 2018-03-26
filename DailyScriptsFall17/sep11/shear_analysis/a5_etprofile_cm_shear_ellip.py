#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 27, 2016
# Last update : Sep 11, 2017 Mon
"""
.. note::

    This program finds ellipticity profile from galshear/galshear_shear.cat.
    This does not change input file, only creates 4 output files.

:Depends: galshear_shear.cat

:Outputs: The outputs are given below::

  color_galshear_shear.dat
  mono_galshear_shear.dat
  color_galshear_ellip.dat
  mono_galshear_ellip.dat

:etprofile: Short description is given below::

	NAME
		etprofile --- calculates tangential alignment profile

	SYNOPSIS
	  etprofile [option...] < catfile > asciifile
	      -o io jo	# origin about which we do profile (2048, 2048)
	      -d dlnr		# log bin size 0.25
	      -r rmin rmax	# min and max radii (200, 2000)
	      -l lossfactor	# multiply e by 1/ lossfactor
	      -e ename	# name for 2-vector ellipticity (e)
	      -x xname	# name for 2-vector spatial coordinate (x)
"""
# Imports
import subprocess
import time

def etprofile_(z):
    """Use etprofile to get four dat files.

    Args:
      z (float): redshift e.g. 0.5, 0.7, 1.0, 1.5

    Outputs:
	  color_galshear_shear.dat
	  mono_galshear_shear.dat
	  color_galshear_ellip.dat
	  mono_galshear_ellip.dat

    """
    # Variables
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # Commands to run
    commands = """
    cd {0}
    etprofile -o 849 849 -d 0.1 -r 100 1200 -e cg_avg < galshear_shear.cat | lc -O > color_galshear_shear.dat ;
    etprofile -o 849 849 -d 0.1 -r 100 1200 -e mg_avg < galshear_shear.cat | lc -O > mono_galshear_shear.dat ;
    lc +all 'ce_avg = %ce %c9e vadd 0.5 vscale' < galshear_shear.cat | etprofile -o 849 849 -d 0.1 -r 100 1200 -e ce_avg | lc -O > color_galshear_ellip.dat   ;
    lc +all 'me_avg = %me %m9e vadd 0.5 vscale' < galshear_shear.cat | etprofile -o 849 849 -d 0.1 -r 100 1200 -e me_avg | lc -O > mono_galshear_ellip.dat
    """.format(pwd)

    print("\nPwd: {} ".format(pwd))
    print("\nCreating:\ncolor_galshear_shear.dat\nmono_galshear_shear.dat\n\
            color_galshear_ellip.dat\nmono_galshear_ellip.dat ")

    # print(commands)
    subprocess.call(commands,shell=True)

def main():
    """Run main function."""
    etprofile_(z='0.5')

if __name__ == "__main__":
    main()
