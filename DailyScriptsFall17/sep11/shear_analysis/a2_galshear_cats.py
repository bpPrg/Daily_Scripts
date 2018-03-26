#!python
# -*- coding: utf-8 -*-
#
# Author      : Douglas Clowe; Associate Professor, Ohio University
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Aug 22, 2016
# Last update : Sep 11, 2017 Mon
"""
.. note::

    1.  This program runs imcat command on all the jedisim output files.
        This reads in following files:
            a. lsst_z0.5_0.fits
            b. lsst90_z0.5_0.fits
            c. mono_z0.5_0.fits
            d. mono90_z0.5_0.fits

        And, also reads two paramters files:
            a. psf10.par
            b. weighted_psf.par


        Then finally create catalogs for each input galaxies like galshear_z0.5_0.cat
        in the output folder **galshear/galshear_cat_z0.5** and so on.


    2.  The parameter files are created using a1_psf10_weighted_psf_par.py.

    3.  To get the weight we first find the average flux ratio of
        f606 and f814 galaxies using ::

            ~/Research/a1_data/average_flux_ratio.py

        Then we got weight range 1.0 to 1.2 using::

            ~/Research/a4b_lsst_jedisim/jedisim/b1_weighted_psf.py

    4.  The psf 10 is chosen as the middle of 21 normalized psf, created by
        Phosim software for narrowband_10.icat and narrowband_10.sed for given seed.
        The Phosim gives unnormalized psf and we normalize all the psf using::

            ~/Research/a3_psf_phosim_flat_sed/psf_phosim_flat_sed/a6_normalize_phosim_psf.py

        so that sum of all the pixels in these psfs are equal to that of psf10.fits.

        We also note that, psf10.fits is same for both normalized and unnormalized cases.

:Inputs: The inputs are given below:
    All jedisim_output fitsfiles
    psf10.par
    weighted_psf.par

:Outputs: galshear/galshear_*.cat


:Runtime: 8 min 9 seconds for 109 loops.

"""
# Imports
import subprocess
import os
import time
import shutil
import re

# beginning time
program_begin_time = time.time()
begin_ctime        = time.ctime()
print('Begin time: ', begin_ctime)


# input/output folder
indir  = '/Users/poudel/Rsh_out/All_jedisim_outputs' # /z0.5/lsst/lsst_z0.5_0.fits


def galshear_cats(z):
    for i in range(0,29+1):
        # output catalog file
        outdir   = 'galshear/galshear_cat_z{}'.format(z)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        ofile    = outdir + '/galshear_z{}_{:d}.cat'.format(z,i)


        # chromatic files
        # /Users/poudel/Rsh_out/All_jedisim_outputs/z0.5/lsst/lsst_z0.5_0.fits
        cfile    = indir + "/z{}/".format(z) + "lsst/lsst_z{}_{:d}.fits".format(z,i)
        c9file   = indir + "/z{}/".format(z) + "lsst90/lsst90_z{}_{:d}.fits".format(z,i)
        cparfile = 'psf/weighted_psf.par'

        # monochromatic files
        mfile    = indir + "/z{}/".format(z) + "mono/mono_z{}_{:d}.fits".format(z,i)
        m9file   = indir + "/z{}/".format(z) + "mono90/mono90_z{}_{:d}.fits".format(z,i)
        mparfile = 'psf/psf10.par'

        # commands to run
        commands = "hfindpeaks " + cfile + " -r 0.5 20 | "                                  + \
        "getsky -Z rg 3 | "                                                                 + \
        "apphot -z 30 -M 30 | "                                                             + \
        "getshapes | "                                                                      + \
        "lc +all 'ox = %x' | "                                                           + \
        "cleancat 5 |  "                                                                    + \
        "apphot -z 30 -M 30 | "                                                             + \
        "getshapes | "                                                                      + \
        "lc +all 'x = %x %d vadd' |  "                                                   + \
        "apphot -z 30 -M 30 | "                                                             + \
        "getshapes | "                                                                      + \
        "lc +all 'x = %x %d vadd' |  "                                                   + \
        "apphot -z 30 -M 30 | "                                                             + \
        "getshapes | "                                                                      + \
        "lc +all 'dx = %x %ox vsub' | "                                                     + \
        "gen2Dpolymodel " + cparfile + " | "                                                + \
        "lc +all 'Pg = %psh %psm %stmod[0] %stmod[1] 2 vector "                          + \
                          "%stmod[2] %stmod[3] 2 vector 2 vector "                          + \
                          "%stmod[4] %stmod[5] 2 vector %stmod[6] "                         + \
                          "%stmod[7] 2 vector 2 vector inverse dot "                        + \
                          "dot msub' 'e = %e %psm %stmod[4] "                               + \
        "%stmod[5] 2 vector %stmod[6] "                                                     + \
        "%stmod[7] 2 vector 2 vector inverse dot "                                          + \
        "%stmod[8] %stmod[9] 2 vector dot vsub' | "                                         + \
        "lc +all 'ce = %e' 'cPg = %Pg' 'cmag = %mag' | "                                 + \
        "apphot -z 30 -M 30 -f " + c9file + " | "                                           + \
        "getshapes -f  "+ c9file + " | "                                                    + \
        "lc +all 'Pg = %psh %psm %stmod[0] %stmod[1] 2 vector %stmod[2] "                + \
                          "%stmod[3] 2 vector 2 vector %stmod[4] "                          + \
                          "%stmod[5] 2 vector %stmod[6] "                                   + \
                          "%stmod[7] 2 vector 2 vector inverse dot dot "                    + \
                          "msub' 'e = %e %psm %stmod[4] %stmod[5] 2 vector "                + \
                          "%stmod[6] %stmod[7] 2 vector 2 vector inverse dot "              + \
                          "%stmod[8] %stmod[9] 2 vector dot vsub' | "                       + \
        "lc +all 'c9e = %e' 'c9Pg = %Pg' 'c9mag = %mag' | "                              + \
        "apphot -z 30 -M 30 -f " + mfile + " | "                                            + \
        "getshapes -f "+ mfile + " | "                                                      + \
        "gen2Dpolymodel " + mparfile + " | "                                                + \
        "lc +all 'Pg = %psh %psm %stmod[0] %stmod[1] 2 vector %stmod[2] "                + \
                          "%stmod[3] 2 vector 2 vector %stmod[4] "                          + \
                          "%stmod[5] 2 vector %stmod[6] "                                   + \
                          "%stmod[7] 2 vector 2 vector inverse dot dot msub' 'e = %e %psm " + \
                          "%stmod[4] %stmod[5] 2 vector %stmod[6] "                         + \
                          "%stmod[7] 2 vector 2 vector inverse dot %stmod[8] "              + \
                          "%stmod[9] 2 vector dot vsub' | "                                 + \
        "lc +all 'me = %e' 'mPg = %Pg' 'mmag = %mag' | "                                 + \
        "apphot -z 30 -M 30 -f " + m9file + "| "                                            + \
        "getshapes -f " + m9file + " | "                                                    + \
        "lc +all 'Pg = %psh %psm %stmod[0] %stmod[1] 2 vector %stmod[2] "                + \
                          "%stmod[3] 2 vector 2 vector %stmod[4] "                          + \
                          "%stmod[5] 2 vector %stmod[6] "                                   + \
                          "%stmod[7] 2 vector 2 vector inverse dot dot msub' 'e = %e %psm " + \
                          "%stmod[4] %stmod[5] 2 vector %stmod[6] "                         + \
                          "%stmod[7] 2 vector 2 vector inverse dot %stmod[8] "              + \
                          "%stmod[9] 2 vector dot vsub' | "                                 + \
        "lc +all 'm9e = %e' 'm9Pg = %Pg' 'm9mag = %mag' > "                              + \
        ofile


        # Print commands into a file
        # print(commands,file=open('dev/commands.sh','w'))

        # run the program
        if not os.path.isfile(ofile):
            print('\nCreating the cat file :', ofile)
            subprocess.call(commands,shell=True)
            pass
##=============================================================================

def main():
    """Run main function."""
    for z in [0.5,0.7,1.0,1.5]:
        galshear_cats(z)


if __name__ == "__main__":
    import time

    # Beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    #  Run the main program
    main()

    # Print the time taken
    program_end_time = time.time()
    end_ctime        = time.ctime()
    seconds          = program_end_time - program_begin_time
    m, s             = divmod(seconds, 60)
    h, m             = divmod(m, 60)
    d, h             = divmod(h, 24)
    print("\nBegin time: ", begin_ctime)
    print("End   time: ", end_ctime, "\n")
    print("Time taken: {0: .0f} days, {1: .0f} hours, \
      {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))
