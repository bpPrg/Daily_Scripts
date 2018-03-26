#!/Users/poudel/anaconda/bin/python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        :
#
"""
 ..note::

    Change the file number in the name of the file.


:Runtime:

"""
# Imports
import re
import glob
import os

def change_filenum():
    for d in ['lsst','lsst90','mono','mono90']:
        for f in glob.glob('z1.5/{}/*.fits'.format(d)):
            # z1.5/mono90/mono90_z1.5_43.fits
            rgx = '(.+?)(\d+)(\.fits)'
            parts = re.search(rgx,f).groups()
            f2 = parts[0] + str(int(parts[1])-10) + parts[2]
            os.rename(f,f2)


def main():
    """Run main function."""
    change_filenum()

if __name__ == "__main__":
    main()
