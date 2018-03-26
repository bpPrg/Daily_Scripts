#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 15, 2016
# Last update : Sep 11, 2017 Mon
"""
.. note::

   This program creates a new dat file with variables
   shear and ellipticity
   by reading only some columns from two input files for
   chromatic and monochromatic cases.

:Depends: This program depends on following:
    color_galshear_shear.dat
    mono_galshear_shear.dat
    color_galshear_ellip.dat
    mono_galshear_ellip.dat

:Outputs: The outputs are in the folder galshear/galshear_cat_z0.5/:
    color_mono_galshear_shear.dat
    color_mono_galshear_ellip.dat

"""
# Imports
import numpy as np
import subprocess
import os
import sys
import shutil

def cm_shear(z):
    # bin   r   ngals   et  eterror   rkappa   kappa  kappaerror  nu
    # 0     1   2       3   4         5        6      7           8
    infile1 = 'galshear/galshear_cat_z{0}/color_galshear_shear.dat'.format(z)
    infile2 = 'galshear/galshear_cat_z{0}/mono_galshear_shear.dat'.format(z)
    r,rkappa,ngals,etmono ,eterrormono  = np.genfromtxt(infile1,delimiter=None,usecols=(1,5,2,3,4),dtype=float,unpack=True)
    r,rkappa,ngals,etcolor,eterrorcolor = np.genfromtxt(infile2,delimiter=None,usecols=(1,5,2,3,4),dtype=float,unpack=True)

    # write to a file
    outfile = 'galshear/galshear_cat_z{0}/color_mono_galshear_shear.dat'.format(z)
    print('Creating : ', outfile)
    with open(outfile,'w') as f:
        # write header
        header = '# r       rkappa     ngals   etmono eterrormono etcolor  eterrorcolor '
        print(header,file=f)

        # write data
        for i in range(len(r)):
            print(r[i],rkappa[i],ngals[i],etmono[i],eterrormono[i],etcolor[i],eterrorcolor[i],sep='   ', file=f)


    # convert dat to cat
    outfile = 'galshear/galshear_cat_z{0}/color_mono_galshear_shear.cat'.format(z)
    print('Creating : ', outfile)
    cmd = 'lc -C -n r -n rkappa -n ngals -n etmono -n eterrormono -n etcolor -n eterrorcolor < galshear/galshear_cat_z{0}/color_mono_galshear_shear.dat > galshear/galshear_cat_z{0}/color_mono_galshear_shear.cat'.format(z)
    subprocess.call(cmd, shell=True)


def cm_ellip(z):
    infile1 = 'galshear/galshear_cat_z{0}/color_galshear_ellip.dat'.format(z)
    infile2 = 'galshear/galshear_cat_z{0}/mono_galshear_ellip.dat'.format(z)
    r,rkappa,ngals,etmono,eterrormono = np.genfromtxt(infile1,delimiter=None,usecols=(1,5,2,3,4),dtype=float,unpack=True)
    r,rkappa,ngals,etcolor,eterrorcolor = np.genfromtxt(infile2,delimiter=None,usecols=(1,5,2,3,4),dtype=float,unpack=True)



    # write to a file
    outfile = 'galshear/galshear_cat_z{0}/color_mono_galshear_ellip.dat'.format(z)
    print('\nCreating : ', outfile)
    with open(outfile,'w') as f:

        # write header
        header = '# r       rkappa     ngals   etmono eterrormono etcolor  eterrorcolor '
        print(header,file=f)

        # write data
        for i in range(len(r)):
            print(r[i],rkappa[i],ngals[i],etmono[i],eterrormono[i],etcolor[i],eterrorcolor[i],sep='   ', file=f)


    # convert dat to cat
    outfile = 'galshear/galshear_cat_z{0}/color_mono_galshear_shear.cat'.format(z)
    print('Creating : ', outfile)
    cmd = 'lc -C -n r -n rkappa -n ngals -n etmono -n eterrormono -n etcolor -n eterrorcolor < galshear/galshear_cat_z{0}/color_mono_galshear_ellip.dat > galshear/galshear_cat_z{0}/color_mono_galshear_ellip.cat'.format(z)
    subprocess.call(cmd, shell=True)

def main():
    """Run main function."""
    cm_shear(z='0.5')
    cm_ellip(z='0.5')

if __name__ == "__main__":
    main()
