#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 27, 2016
# Last update : Sep 11, 2017 Mon
"""
.. note::

   This program creates the shear and ellip cat files from dat files.

:Depends: This program depends on following:
    color_mono_galshear_shear.dat
    color_mono_galshear_ellip.dat

:Outputs: The outputs are in the folder galshear/galshear_cat_z0.5/:
    color_mono_galshear_shear.cat
    color_mono_galshear_ellip.cat

"""
# Imports
import subprocess
import time


def cm_shear_ellip(z):
    """Create shear and ellip catalog files.

    Args:
      z (float): redshift e.g. 0.5, 0.7, 1.0, 1.5

    Outputs:
      color_mono_galshear_shear.cat
      color_mono_galshear_ellip.cat

    """
    # Variables
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # Commands to run
    commands = """
    cd {0}
    lc -C -n r -n rkappa -n ngals -n gm -n gmerr -n gc -n gcerr < color_mono_galshear_shear.dat > color_mono_galshear_shear.cat ;
    lc -C -n r -n rkappa -n ngals -n em -n emerr -n ec -n ecerr < color_mono_galshear_ellip.dat > color_mono_galshear_ellip.cat
    """.format(pwd)

    print("\nCreating galshear/color_mono_galshear_shear.cat ")
    print("Creating galshear/color_mono_galshear_ellip.cat ")

    # print(commands)
    subprocess.call(commands,shell=True)


def main():
    """Run main function."""
    cm_shear_ellip(z='0.5')

if __name__ == "__main__":
    main()
