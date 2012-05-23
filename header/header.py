#!/usr/bin/python
""" Prints header of a FITs file """
import sys
import pyfits

file = sys.argv[1]

if len(sys.argv) == 3:
    secondary = sys.argv[2]
else:
    secondary = 0

print file
hdu = pyfits.open(file)
print hdu[int(secondary)].header

