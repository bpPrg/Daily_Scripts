#!python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Aug 24, 2016
# Last update : Sep 11, 2017 Mon
"""
.. note::

    1. This program creates fitted P gamma values (i.e. galshear_fpg.cat)
       from galshear_cut.cat and 8 other par files.
    2. It will also create shear catalog file.

:Depends: Depends of following files:
  galshear/galshear_cut.cat
  galshear/galshear_*.par  # 8 par files for monochromatic and chromatic

  i.e. ::

    galshear_c9pg0.par  galshear_cpg0.par   galshear_m9pg0.par  galshear_mpg0.par
    galshear_c9pg1.par  galshear_cpg1.par   galshear_m9pg1.par  galshear_mpg1.par

    Also, galshear_big_cat and galshear_cut.cat

:Output: Ouptputs are:
  galshear/galshear_fpg.cat
  galshear/galshear_shear.cat


:Runtime: 9 seconds
"""
# Imports
import subprocess
import time


def fitted_Pgamma(z):
    """Create fitted Pgamma cat file for given redshift.

    Args:
      z (float): redshift e.g. 0.5, 0.7, 1.0, 1.5

    Outputs:
      galshear_fpg.cat

    """
    # Variables
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # Commands to run
    commands = """
    cd {0}
    lc +all 'ox = %x' 'x = %rg %e[0] 2 vector' < galshear_cut.cat | gen2Dpolymodel galshear_mpg0.par | gen2Dpolymodel galshear_m9pg0.par | gen2Dpolymodel galshear_cpg0.par | gen2Dpolymodel galshear_c9pg0.par | lc +all 'x = %rg %e[1] 2 vector' | gen2Dpolymodel galshear_mpg1.par | gen2Dpolymodel galshear_m9pg1.par | gen2Dpolymodel galshear_cpg1.par | gen2Dpolymodel galshear_c9pg1.par | lc +all 'x = %ox' > galshear_fpg.cat
    """.format(pwd)

    print("\nCreating fitted Pgamma cat file galshear_fpg.cat for redshift {0}:\n".format(z))
    print(commands)
    subprocess.call(commands,shell=True)




def shear(z):
    """Create Pgamma par files for chromatic, monochromatic and their rotated cat files.

    Args:
      z (float): redshift e.g. 0.5, 0.7, 1.0, 1.5

    Outputs:
      galshear_shear.cat

    """
    # Variables
    pwd = "galshear/galshear_cat_z{0}".format(z)

    # Commands to run
    commands = """
    cd {0}
    lc +all 'mg = %me[0] %mPg0mod / %me[1] %mPg1mod / 2 vector' 'm9g = %m9e[0] %m9Pg0mod / %m9e[1] %m9Pg1mod / 2 vector' 'cg = %ce[0] %cPg0mod / %ce[1] %cPg1mod / 2 vector' 'c9g = %c9e[0] %c9Pg0mod / %c9e[1] %c9Pg1mod / 2 vector' < galshear_fpg.cat | lc +all 'mg_avg = %mg %m9g vadd 0.5 vscale' 'cg_avg = %cg %c9g vadd 0.5 vscale' > galshear_shear.cat
    """.format(pwd)

    print("\nCreating fitted Pgamma cat file galshear_shear.cat for redshift {0}:\n".format(z))
    print(commands)
    subprocess.call(commands,shell=True)



def main():
    """Run main function."""
    # fitted_Pgamma(z='0.5')
    shear(z='0.5')

if __name__ == "__main__":
    main()
