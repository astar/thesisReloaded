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



def main():
    """ Testing Docstring"""

    file = sys.argv[1]
    fit_file =  sys.argv[2]

    xdata, ydata  = read_fits(file)
    fit = np.genfromtxt(fit_file , delimiter=',', dtype=None)
    fit_files = [row[0] for row in fit] # generate list of files to
    fit_files = [x.strip(' ') for x in fit_files]
    p = get_poly(file, fit_files, fit)
    f = lambda x: p[0] + p[1]*x + p[2]*x**2 + p[3]*x**3 + p[4]*x**4

#    import ipdb; ipdb.set_trace()

#    write_fits(file, ydata/f(xdata) )
    print file
    plot(file,xdata,ydata,ydata/f(xdata),6553)


def plot(file,xdata,ydata,f,spLine):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    graph1 = ax1.plot(xdata,ydata, 'r')

    ax2 = fig.add_subplot(212, sharex=ax1)
    graph2 = ax2.plot(xdata,f, 'b')

    ax1.set_title(file)
    ax1.set_xlabel("$Wavelenght [\\AA]$")
    ax1.set_ylabel("$Energy [10^{-17} erg/s/cm^2/\\AA]$")
#    ax1.axvline(x=spLine, color = 'g', ls ='--')
#    ax2.axvline(x=spLine, color = 'g', ls ='--')
    plt.show()


def write_fits(file, norm):
    hdu = pyfits.open(file, mode = 'update')
    data = hdu[1].data
    data.field('FLUX')[:] = norm
    hdu[0].header.add_history('normalized')
    hdu.flush()

def read_fits(file):
    hdu = pyfits.open(file)
    data = hdu[1].data
    x = data.field('WAVE')
    y = data.field('FLUX')
    return np.asarray([x, y])

def get_poly(file, fit_files, fit):
    try:
        index = fit_files.index(file)
    except:
        print "no fit data for {}".format(file)
        sys.exit(1)
    return [fit[index][1], fit[index][2], fit[index][3], fit[index][4], fit[index][5]]


if __name__=='__main__':
    main()
