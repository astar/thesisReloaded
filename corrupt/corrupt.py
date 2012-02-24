#!/usr/bin/python
import sys, pyfits, numpy as np

Halpha = 6564.614
 
file = sys.argv[1]
data = pyfits.getdata(file)
sigma = data[4]


w = lambda x : 10.0**(3.5796 + x*10.0**(-4))
x = np.arange(1,data[0].size + 1)
xx  = w(x) # convert to actual wavelenght

sigma2 = sigma[(xx < Halpha + 25) & (xx > Halpha - 25)]
if not sigma2.any():
    f = open('corrupt.log','a')
    f.write(file + '\n')
    f.close()
