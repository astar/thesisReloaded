#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
normalize fits save and plot the result
"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 20012-3012 Astar'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/


import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np
import pyfits
import sys
import csv
import re
import os
import subprocess as sp


def main():
    """ Open fits in DR8 format and takes max/min around H alpha line """

    file = sys.argv[1]

    xdata, ydata  = read_fits(file)

    line = 6563
    range = 50

    extrem = get_Max(xdata, ydata, line, range)
    log('extrem','{},{}'.format(file, extrem))


def read_fits(file):
    hdu = pyfits.open(file)
    data = hdu[1].data
    x = data.field('wavelength')
    y = data.field('FLUX')
    return np.asarray([x, y])

def get_Max(x, y, line, range):
    x_min = line - range
    x_max = line + range
    x_range = x[(x > x_min) & (x < x_max)]
    y_range = y[(x > x_min) & (x < x_max) ]
    y_med = np.median(y)
    y_max = max(y_range)

    if y_max > y_med:
        ret = y_max - y_med
    else:
        ret = y_min - y_med

    return str(ret)

def log(logFile, line):
        f = open(logFile + '.log','a')
        f.write(line + '\n')
        f.close()

if __name__=='__main__':
    main()
