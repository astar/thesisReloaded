# library to convert ra, dec to degrees
# based on http://www.atnf.csiro.au/people/Enno.Middelberg/python/python.html
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
