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
import cfg

def main():
    # Read configuration
    try:
        mode = cfg.mode 
        limit = cfg.exp 
        dir = cfg.input_dir
        dest = cfg.dest_dir
    except Exception, e:
        print "Error reading config parameters"
        sys.Exit(1)

    fits =  glob(dir + '/*/*/*.fits')
    if mode == 'n':
        ab_normal = [f for f in fits if not is_normalized(get_flux(f)) ]

    elif mode == 'e':
        ab_normal = [f for f in fits if is_exposition_short(get_exposition(f), limit) ]

    else:
        print 'Uknown modus operandi'
        sys.Exit(1)
        
    # create dest dir
    create_dir(dest)

    #make dirs
    full_dest_dirs = [(os.path.split(f)[0]).replace(dir, dest) for f in ab_normal ]
    #make them unique
    full_dest_dirs = list(set(full_dest_dirs))
    [create_dir(d) for d in full_dest_dirs]

    #move abnormal files 
    [move(d, d.replace(dir, dest)) for d in ab_normal]
    print 'Moved {} abnormal files, into {} directory'.format(len(ab_normal),dest)
    
    #remove empty dirs
    
    dirs_to_check = [os.path.split(f)[0] for f in fits]
    #make them unique
    dirs_to_check = list(set(dirs_to_check))
    
    [remove_empty_dir(d) for d in dirs_to_check]
    
    # move png
    #    [move(s + '.png', (s + '.png').replace(dir, dest)) for s in ab_normal]

def get_flux(file):
    f = pf.open(file)
    hdu = f[1]
    data = hdu.data
    return data["FLUX"]

def get_exposition(file):
    f = pf.open(file)
    hdu = f[0]
    data = hdu.header
    return data["EXPTIME"]

    
def is_normalized(y):
    return np.median(y[:100]) < 10

def is_exposition_short(e, limit):
    return e < limit

    
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


def remove_empty_dir(name):
    if  not os.listdir(name):
        try:
            s.rmtree(name)
            
        except IOError:
            print "Could not remove dir %s!" % name
            
def move(src, dest):
    try:

        s.move(src, dest)
        return True

    except IOError:
        print "Could not move  dir! src = {}, dest = {}".format(src, dest)

if __name__ == '__main__':
    main()