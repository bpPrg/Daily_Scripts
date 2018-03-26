#!python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Sep 27, 2016
# Last update : Sep 11, 2017 Mon
"""
.. note::

   This program creates the pdf of the plots for shear analysis.
   It will first create postscript files using imcat tool plotcat.
   Then will transform ps to pdf using the tool ps2pdf.
   Then it will combine pdfs using ghostscript command.

   Note that plotcat uses pgplot and we should have installed it first befre
   using this program.
   `pgplot website <http://www.astro.caltech.edu/~tjp/pgplot/macos/>`

:Depends: This program depends on following:
    color_mono_galshear_shear.cat
    color_mono_galshear_ellip.cat

:Outputs: The outputs are in the folder plots/galshear_plots_z0.5/:
    There are 6 output plots for ps, pdf and finally only one combined pdf.
    r_gm_shear.ps     r_gm_shear.pdf
    r_gc_shear.ps     r_gc_shear.pdf
    r_erat_shear.ps   r_erat_shear.pdf
    r_em_ellip.ps     r_em_ellip.pdf
    r_erat_ellip.ps   r_erat_ellip.pdf
    r_erat_ellipp.ps  r_erat_ellipp.pdf

    shear_analysis_z0.5.pdf

:Commands: The commands used are::

    plotcat r gm -w 3  -T 'shear analysis for default'  -d 'r_gm_shear.ps/ps'  <  color_mono_galshear_shear.cat
    ps2pdf r_gm_shear.ps r_gm_shear.pdf


"""

# Imports
import subprocess
import os


def plots(z):
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # input catalogs
    incat1 = '{}/color_mono_galshear_shear.cat'.format(pwd)
    incat2 = '{}/color_mono_galshear_ellip.cat'.format(pwd)

    # Plot path
    plot_path = 'plots/galshear_plots_z{}'.format(z)
    if not os.path.isdir(plot_path):
        os.makedirs(plot_path)


    ## plots for shear and ellipticity
    cmd1 = "plotcat r gm -w 3                       -T 'shear analysis for default' "       + " -d '{}/r_gm_shear.ps/ps' ".format(plot_path)    + " <  " + incat1
    cmd2 = "plotcat r gc -w 3                       -T 'shear analysis for default' "       + " -d '{}/r_gc_shear.ps/ps' ".format(plot_path)    + " <  " + incat1
    cmd3 = "plotcat r 'erat = %gc %gm - %gm /' -w 3 -T 'shear analysis for default' "       + " -d '{}/r_erat_shear.ps/ps' ".format(plot_path)  + " <  " + incat1
    cmd4 = "plotcat r em -w 3                       -T 'ellipticity analysis for default' " + " -d '{}/r_em_ellip.ps/ps' ".format(plot_path)    + " <  " + incat2
    cmd5 = "plotcat r 'erat = %ec %em /' -w 3       -T 'ellipticity analysis for default' " + " -d '{}/r_erat_ellip.ps/ps' ".format(plot_path)  + " <  " + incat2
    cmd6 = "plotcat r 'erat = %ec %em - %em /' -w 3 -T 'ellipticity analysis for default' " + " -d '{}/r_erat_ellipp.ps/ps' ".format(plot_path) + " <  " + incat2


    # cmds to plot
    commands = [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6]
    for cmd in commands:
        subprocess.call(cmd,shell=True)

    print('ps files created inside the directory: {}'.format(plot_path))

    # open image
    cmd = "open {}/r_gm_shear1.ps ".format(plot_path)
    subprocess.call(cmd, shell=True)

def main():
    """Run main function."""
    plots(z='0.5')

if __name__ == "__main__":
    main()
