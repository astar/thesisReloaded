#!/usr/bin/python
""" Check fits file for some sequence of zeros in sigam around Halpha line. 
This should corespond to the corrupted spectrum """


import sys, pyfits, numpy as np

deli = ' '
Halpha = 6564.614

if len(sys.argv) > 1:
    file = sys.argv[1] 
    logFile = sys.argv[2]
else:
    sys.exit(1)

hdu = pyfits.open(file)
data = hdu[1].data
header = hdu[1].header
data = pyfits.getdata(file)
sigma = data.field('inverse_variance')
x = data.field('wavelength')

range = 5
sigma2 = sigma[(x < Halpha + range) & (x > Halpha - range)]


def zeros(sigma,x, Halpha):
    """ Test how many zeros are to the left """
    index = 0
    while not sigma[(x < Halpha + index) & (x > Halpha - index)].any():
        index +=1
        if index/2 > len(sigma):
            break
    return index/2

def row(items):
    r = ''
    for item in items:
        r = r + deli + str(item)
    return r + '\n'

if not sigma2.any():
    z = zeros(sigma,x,Halpha)
    f = open(logFile + '.log','a')
    f.write(row([file, z, header['MJD'],header['PLATEID'],header['FIBERID']]))
    f.close()


