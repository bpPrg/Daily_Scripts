#!/Users/poudel/anaconda/bin/python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Sep 11, 2017 Mon
# Last update :
# Est time    :

# Imports
import os
import glob
import subprocess

def delete_string():
    for f in glob.glob('*.rst'):
        cmd = """sed -ie '1s/module//' {}""".format(os.path.basename(f))
        print(cmd)
        subprocess.call(cmd, shell=True)
        subprocess.call('rm {}'.format(os.path.basename(f)+'e'), shell=True)


def main():
    """Run main function."""
    delete_string()

if __name__ == "__main__":
    main()
