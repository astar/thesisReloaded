#!/usr/bin/python
""" Check fits file for some sequence of zeros in sigam around Halpha line. 
This should corespond to the corrupted spectrum """


import sys, pyfits, numpy as np, os, glob

Halpha = 6564.614
range = 5

def main():

    if len(sys.argv) > 1:
        dir = sys.argv[1] 
        logFile = sys.argv[2]
    else:
        sys.exit(1)
    
    files = listdir(dir)
    nFiles = len(files)
    for idx, file in enumerate(files):
        (data, header) = fitsInfo(file)
        (c, status) = corrupt(data)
        if c:
            log(logFile, line(file, header, status))
        print '(%i/%i) %s %s' % (idx + 1, nFiles, file, status)

def line(file, header, z):
    deli = ' '
    r = ''
    items = [file, str(z), str(header['MJD']),str(header['PLATEID']),str(header['FIBERID'])]
    r = deli.join(items)
    return r + '\n'


    

def fitsInfo(file):
    hdu = pyfits.open(file)
    data = hdu[1].data
    header = hdu[1].header
    data = pyfits.getdata(file)
    return data, header
    
def corrupt(data):
    """Check fits file for zeros in inverse varience """
    sigma = data.field('inverse_variance')
    x = data.field('wavelength')
    
    
    sigma2 = sigma[(x < Halpha + range) & (x > Halpha - range)]

    if not sigma2.any():
        if not sigma.any():
            z = len(sigma)
        else:
            z = zeros(sigma,x,Halpha)

        return True, str(z)
    return False, 'ok'

def log(logFile, line):            
        f = open(logFile + '.log','a')
        f.write(line)
        f.close()

def listdir(d):
    return glob.glob(d + '/*.fits')

def zeros(sigma,x, Halpha):
    """ Test how many zeros are to the left """
    index = 0
    while not sigma[(x < Halpha + index) & (x > Halpha - index)].any():
        index +=1
        if index/2 > len(sigma):
            break
    return index/2



if __name__ == "__main__":
    main()
