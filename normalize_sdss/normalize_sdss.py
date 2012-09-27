#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
normalize fits save and plot the result
"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 20012-3012 Astar'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/



import numpy as np
import sys
import pyfits
import csv
import re
import os
import subprocess as sp


def main():
    """ Testing Docstring"""

    file = sys.argv[1]

    xdata, ydata  = read_fits(file)

    n = normalize(file, xdata)

    write_fits(file, ydata/n )
    print "{} done".format(file)

def write_fits(file, norm):
    hdu = pyfits.open(file, mode = 'update')
    data = hdu[1].data
    data.field('FLUX')[:] = norm
    hdu[0].header.add_history('normalized')
    hdu.flush()

def read_fits(file):
    hdu = pyfits.open(file)
    data = hdu[1].data
    x = data.field('wavelength')
    y = data.field('FLUX')
    return np.asarray([x, y])

def normalize(file, data):
    try:
        fit = sp.Popen(['./fitfits',file ],stdout = sp.PIPE)
        out, err = fit.communicate()
        p = out.strip().split(',')
        f = lambda x: float(p[1]) + float(p[2])*x + float(p[3])*x**2 + float(p[4])*x**3 + float(p[5])*x**4
        return f(data)
    except:
        print "problem getting fit for  {}".format(file)
        log('errors',file)
        sys.exit(1)


def log(logFile, line):
        f = open(logFile + '.log','a')
        f.write(line + '\n')
        f.close()

if __name__=='__main__':
    main()
