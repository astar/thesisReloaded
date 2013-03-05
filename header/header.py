#!/usr/bin/python
""" Prints header of a FITs file """
import sys
import pyfits

file = sys.argv[1]

hdu = pyfits.open(file)

if len(sys.argv) == 3:
    print hdu[0].header[sys.argv[2]]
else:
    print hdu[0].header
