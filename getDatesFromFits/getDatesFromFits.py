#!/usr/bin/python
""" produce list of max DATE-OBS from fits files """
import sys
import os
import pyfits
from glob import glob
from dateutil import parser
main_dir = sys.argv[1]


def getHeader(file):
    return pyfits.open(file)

def getDate(file):
    hdu = getHeader(file)
    return parser.parse(hdu[0].header['DATE-OBS'])

def getRaDec(file):
    hdu = getHeader(file)
    ra = hdu[0].header['RA']
    dec = hdu[0].header['DEC']
    return ra + ',' + dec

    
def getMaxDate(dir): 
    files = glob(os.path.join(dir, '*.fits'))
    dates = [getDate(file) for file in files]
    max_date = max(dates)
    diff = parser.parse("6.9.2012") - max_date
    diff = diff.days
    dir_name = os.path.split(dir)[-1]
    radec = getRaDec(files[0])
    return  dir_name + ',' + radec + ',' + str(diff) + '\n'

dir_dates = [getMaxDate(dir) for dir in glob(main_dir)]
f = open('dir_dates.csv','w')
f.writelines(dir_dates)
f.close()
