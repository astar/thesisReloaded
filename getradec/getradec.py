#!/usr/bin/python
""" Prints ra,dec of a FITs file """
import os
import re
import sys
import pyfits
import sys
import string


def dec2deg(inp):
    dec=string.split(inp, ":")
    hh=abs(float(dec[0]))
    mm=float(dec[1])/60
    ss=float(dec[2])/3600
    if float(dec[0]) < 0:
        sgn = '-'
    else:
        sgn = ''

    return sgn + str(hh+mm+ss)

def ra2deg(inp):
    ra=string.split(inp, ":")
    hh=abs(float(ra[0]))*15
    mm=float(ra[1])/60*15
    ss=float(ra[2])/3600*15


    return  str(hh+mm+ss)

file = sys.argv[1]

if len(sys.argv) == 3:
    secondary = sys.argv[2]
else:
    secondary = 0


hdu = pyfits.open(file)
hdr = hdu[int(secondary)].header
file_info = file.replace('/',',')
#import ipdb;ipdb.set_trace()

ra = hdr['RA']
if re.search('pyfits', str(ra)):
    ra = hdr['CAT-RA']

dec = hdr['DEC']
if re.search('pyfits', str(dec)):
    dec = hdr['CAT-DEC']

print '{},{},{},{},{},{}'.format(file_info, hdr['OBJECT'], ra, dec,ra2deg(ra), dec2deg(dec))
