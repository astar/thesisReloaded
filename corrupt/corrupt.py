#!/usr/bin/python
""" Check fits file for some sequence of zeros in sigam around Halpha line. 
This should corespond to the corrupted spectrum """


import sys, pyfits, numpy as np, os

def main():

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

    if not sigma2.any():
        if not sigma.any():
            z = len(sigma)
        else:
            z = zeros(sigma,x,Halpha)
            
        f = open(logFile + '.log','a')
        f.write(row([file, str(z), str(header['MJD']),str(header['PLATEID']),str(header['FIBERID'])]))
        f.close()

def listdir(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def zeros(sigma,x, Halpha):
    """ Test how many zeros are to the left """
    index = 0
    while not sigma[(x < Halpha + index) & (x > Halpha - index)].any():
        index +=1
        if index/2 > len(sigma):
            break
    return index/2



def row(items):
    deli = ' '
    r = ''
    for item in items:
        r = deli.join(items)
    return r + '\n'




if __name__ == "__main__":
    main()
