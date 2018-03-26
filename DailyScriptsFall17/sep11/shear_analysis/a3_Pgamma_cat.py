#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Aug 24, 2016
# Last update : Sep 10, 2017 Sun
"""
.. note::

    This program creates P_gamma values (Pg0 and Pg1)
    for chromatic and monochromatic fitsfiles. (c,c9,m,m9)

    The suffix 9 is for 90 degree rotated case.

    In total it creates 2*4 = 8 par files inside galshear.
    Also, in the end it creates two cat files::

      galshear/galshear_big.cat
      galshear/galshear_cut.cat

    This means in total 2*4 = 8 + 2 = 10 files are created.

:Depends:
  galshear/galshear_*.cat

:Outputs:
  inside galshear 8 par files::

    galshear_c9pg0.par  galshear_cpg0.par   galshear_m9pg0.par  galshear_mpg0.par
    galshear_c9pg1.par  galshear_cpg1.par   galshear_m9pg1.par  galshear_mpg1.par

  Also, galshear_big_cat and galshear_cut.cat


:Runtime: 8 min 9 seconds for 109 loops.
"""
# Imports
import subprocess
import time


def bigcat_cutcat(z):
    """Create big cat file and also create modified cut of it."""

    # Variables
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # Commands to Run
    commands= """
    cd {0}
    catcats galshear_z{1}_[0123456789].cat galshear_z{2}_[123456789].cat galshear_z{3}_[0123456789].cat > galshear_big.cat
    lc -c < galshear_big.cat
    lc -i '%rg 1.5 > %ce %ce dot 1 < and %me %me dot 1 < and %c9e %c9e dot 1 < and %m9e %m9e dot 1 < and' < galshear_big.cat > galshear_cut.cat
    """.format(pwd,z,z,z)

    print("\nRunning catcats to get big cat file :\n")
    print(commands)
    subprocess.call(commands,shell=True)



def Pgamma(z,x):
    """Create P_gamma par files for chromatic, monochromatic and their rotated cat files.

    Args:
      pwd (str): present working directory e.g. galshear/galshear_cat_z0.5
      z (float): redshift e.g. 0.5, 0.7, 1.0, 1.5
      x (str): either of letter 'c', 'c9', 'm', or 'm9'  eg. x = 'c'

    Outputs:
      galshear_cpg0.par cpg1.par etc.

    """
    # Variables
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # Commands to run
    commands = """
    cd {0}
    lc +all 'x = %rg %{1}e[0] 2 vector' '{1}Pg0 = %{1}Pg[0][0]' < galshear_cut.cat | fit2Dpolymodel2 x 4 1 {1}Pg0 > galshear_{1}pg0.par
    lc +all 'x = %rg %{1}e[1] 2 vector' '{1}Pg1 = %{1}Pg[1][1]' < galshear_cut.cat | fit2Dpolymodel2 x 4 1 {1}Pg1 > galshear_{1}pg1.par
    """.format(pwd,x)

    print("\nCreating Pgamma par files for {0}pg0 and {0}pg1 for redshift {1}:\n".format(x,z))
    print(commands)
    subprocess.call(commands,shell=True)

def create_pars():
    # for z in [0.5,0.7,1.0,1.5]:
    for z in [0.5]:
        for x in ['c','c9','m','m9']:
            Pgamma(z,x)

def main():
    """Run main function."""
    # First create big_cat and cut_cat
    # bigcat_cutcat('0.5')

    # Then create Pgamma par files.
    create_pars()

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
