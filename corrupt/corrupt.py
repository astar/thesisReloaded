#!/usr/bin/python
import sys, pyfits, numpy as np

Halpha = 6564.614
 
logFile = sys.argv[2]
file = sys.argv[1]
hdu = pyfits.open(file)
data = hdu[1].data

data = pyfits.getdata(file)
sigma = data.field('inverse_variance')
x = data.field('wavelength')

range = 50
sigma2 = sigma[(x < Halpha + range) & (x > Halpha - range)]
if not sigma2.any():
    f = open(logFile + '.log','a')
    f.write(file + '\n')
    f.close()
