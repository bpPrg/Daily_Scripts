#!python
# -*- coding: utf-8 -*-
#
# Author      : Douglas Clowe; Associate Professor, Ohio University
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Aug 22, 2016
# Last update : Sep 11, 2017 Mon

"""Create parameter files for psf10.fits and weighted_psf.fits using IMCAT.

The par files contain quantities l, m, and st.
l and m has values 0.
The vector st has 11 components.

:Inputs: psf10.fits, weighted_psf.fits

:Outputs: psf10.par, weighted_psf.par


:Info:

    1. This program takes in an input fitsfile and creates a parameter file
       for that file.

    2. weighted_psf.fits is created from weighted average of 21 normalized psfs
       in between weights 1 and 1.2.::

         ( ref: ~/Research/a4b_lsst_jedisim/jedisim/b1_weighted_psf.py)
         ( ref: ~/Research/a1_data/average_flux_ratio.py)

    3. psf10.fits is the unnormalized (same as normalized ) psf created by phosim. We use this psf
       to normalize all the 21 unnormalized psfs created by phosim.

    4. psrat is the pixscale ratio.::

         from jedisim_config_file:
         pix_scale=0.06  		# pixel scale used in jedisim
         final_pix_scale=0.2    # LSST pixscale (arcsecords per pixel)

         psrat = 0.06 / 0.2 = 0.3

:Runtime: 24 seconds on Sep 10, 2017 Sun (Pisces)

"""


# Imports
from __future__ import print_function
import os
import sys
import subprocess
import time

def par_lmst(sfile,psrat,ffile,ofile):
    """Create par files for given input fits files.

    Args:
      sfile (string): psf/psf10
      psrat (float): pixscale ratio 0.06/0.2 = 0.3
      ffile (string): psf/psf10.fits
      ofile (string): psf/psf10.par

    """

    ## Do imcat analysis
    commands = r"""
    ic -s 100 '%1 grand .001 * +' {}  > temp.fits ;
    hfindpeaks temp.fits -r 0.5 20 |
    getsky -Z rg 3 |
    apphot -z 30 |
    lc -i '%flux 0 >' |
    cleancat 100000 |
    getshapes -s {:.1f}  |
    lc +all 'x = %x %d vadd' |
    apphot -z 30 |
    getshapes -s  {:.1f} |
    lc +all 'x = %x %d vadd' |
    apphot -z 30 |
    getshapes -s {:.1f} |
    lc +all 'x = %x %d vadd' |
    apphot -z 30 |
    getshapes -s  {:.1f} |
    lc +all 'st = %psh[0][0] %psh[0][1] %psh[1][0] %psh[1][1] %psm[0][0] %psm[0][1] %psm[1][0] %psm[1][1] %e[0] %e[1] %rg 11 vector' |
    fit2Dpolymodel x 0 0 st > {}  ;
    rm temp.fits
    """.format(ffile,psrat,psrat,psrat,psrat,ofile)


    # Print the commands
    print("\nRunning commands :\n")
    print('Commands : \n', commands)
    print("\n\n")
    subprocess.call(commands,shell=True)

def main():
    """Run main function."""

    # psf10.fits
    sfile = 'psf/psf10'
    psrat = 0.3   # ratio of pixscales 0.06/0.2 = 0.3
    ffile = 'psf/psf10.fits'
    ofile = 'psf/psf10.par'
    par_lmst(sfile,psrat,ffile,ofile)

    # weighted_psf.fits
    sfile = 'psf/weighted_psf'
    psrat = 0.3   # ratio of pixscales 0.06/0.2 = 0.3
    ffile = 'psf/weighted_psf.fits'
    ofile = 'psf/weighted_psf.par'
    par_lmst(sfile,psrat,ffile,ofile)

if __name__ == "__main__":
    # Start time
    start_time = time.time()

    # Run main
    main()
    # Print the time taken
    end_time = time.time()
    seconds  = end_time - start_time
    m, s     = divmod(seconds, 60)
    h, m     = divmod(m, 60)
    d, h     = divmod(h, 24)
    print("\nTime taken ==> {:2.0f} days, {:2.0f} hours,\
    {:2.0f} minutes, {:f} seconds.".format( d, h, m, s))
