#!/usr/bin/python
""" Prints ra,dec of a FITs file """
import os
import sys
import pyfits

file = sys.argv[1]

if len(sys.argv) == 3:
    secondary = sys.argv[2]
else:
    secondary = 0


hdu = pyfits.open(file)
hdr = hdu[int(secondary)].header
print '{},{},{},{}'.format(file, hdr['OBJECT'], hdr['RA'], hdr['DEC'])