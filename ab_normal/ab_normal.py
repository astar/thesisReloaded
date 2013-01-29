#!/usr/bin/env python


"""
Simply test if apectrum is succesfully normalized 
"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 2013 Jaroslav Vazny'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/

import pyfits as pf
import numpy as np
import os
import sys
import shutil as s
from glob import glob

def main():
    dir = sys.argv[1] # first agument is name of input directory
    fits =  glob(dir + '/*/*/*.fits')

    normalized = [is_normalized(get_flux(f)) for f in fits]
    ab_normal = [os.path.split(fits[i])[0] for i, x in enumerate(normalized) if not x]

    # create dest dir
    dest = 'ab_normal'
    create_dir(dest)

    # move directory of abnormal spectrum
    #import ipdb;ipdb.set_trace() 
    [move(d, d.replace(dir, dest)) for d in ab_normal]

    # move png
    [move(s + '.png', (s + '.png').replace(dir, dest)) for s in ab_normal]
      
def get_flux(file):
    f = pf.open(file)
    hdu = f[1]
    data = hdu.data
    return data["FLUX"]

def is_normalized(y):
    return np.median(y[:100]) < 10

def create_dir(name):
    if not os.path.exists(name):
        try:
            os.makedirs(name)
        except IOError:
            print "Could not create dir %s!" % name
    

def remove_dir(name):
    if  os.path.exists(name):
        try:
            s.rmtree(name)
            
        except IOError:
            print "Could not remove dir %s!" % name

def move(src, dest):
    try:
        s.move(src, dest)
        return True

    except IOError:
        print "Could not move  dir!"

if __name__ == '__main__':
    main()