#!/usr/bin/python
""" check fits files for update throught ssa protocol
Program does
------------
* find max dates of fits files in structure category/star/observations.fits
* convert ra, dec --> deg
* ssa query --> votable
* analyze votable
* download fits
"""
import re
import os
import sys
import pyfits as pf
from dateutil import parser
import string
import urllib2

# config
sep1 = 40*'-'
sep2 = 40*'='
sep3 = 40*'*'
ISO_8601 = '%Y-%m-%d'
h_alpha = 6563
ssa = 'http://ssaproxy.asu.cas.cz/ccd700/q/pssa/ssap.xml?POS={},{}&SIZE=0.01&REQUEST=queryData&FLUXCALIB=normalized&BAND=6500e-10/6700e-10&format=fits&TIME={}/'

def main():

    if len(sys.argv) > 1:
        thedir = sys.argv[1]
    else:
        print 'First agrument is the input dir'
        sys.exit(1)

    Category(thedir)


class Category(list):

    def dir_list(self, thedir):
        return [name for name in os.listdir(thedir)
                if os.path.isdir(os.path.join(thedir, name))]

    def __init__(self, cat_path):
        self.thedir = cat_path
        self.name = os.path.basename(cat_path)
        self.dirs = self.dir_list(cat_path)
        self.stars = [Star(cat_path, star) for star in self.dirs]
        self.count = len(self.stars)
        print sep2

        print "Added category {} with {} members".format(self.name, self.count)

    def __repr__(self):
        return str(self.name)
    __str__ = __repr__


class Star(list):

    def parse_votable(self, text):
        """ extract file names form votable """
        try:
            fits = re.findall(
        'http://ssaproxy.asu.cas.cz/getproduct/ccd700/data/.{,40}fits[^<]{,50}',
            text)
            return fits
        except:
            print "No newer files"

            
        
    def check_ssa(self):
        """ download votable of
            newer fits than stored
        """
        ssa.format(self.ra2deg(self.ra),
                   self.dec2deg(self.dec),
                   self.max_date.strftime(ISO_8601))
        try:
            s = urllib2.urlopen(ssa)
            return s.read()

        except IOError:
            print "Could not download file"

        finally:
            s.close()
                
    def dec2deg(self, dec):
        """ converts dec to degrees
        """
        dec = string.split(dec, ":")
        hh = abs(float(dec[0]))
        mm = float(dec[1])/60
        ss = float(dec[2])/3600
        deg = str(hh+mm+ss)
        if float(dec[0]) < 0:
                deg += "-" 
        return deg
        
    def ra2deg(self, ra):
        """ converts ra to degrees
        """
        ra = string.split(ra, ":")        
        hh = float(ra[0])*15
        mm = (float(ra[1])/60)*15
        ss = (float(ra[2])/3600)*15
        return str(hh+mm+ss)

    def file_list(self, thedir):
        f = lambda thedir, name: os.path.join(thedir,
                                              name)
        return [name for name in
                os.listdir(thedir)
                if os.path.isfile(f(thedir, name))
                and os.path.splitext(f(thedir, name))[1] == '.fits']

    def load_spectra(self):
        self.dates = []
        for sp in self.spectra:
            sp.read_spectrum()
            self.dates.append(sp.date)

        
        self.loaded = True
        return True

    def statistics(self):
        t = " Star: {}\n Count: {}\n First: {}\n Last: {}\n Diff: {} days\n"
        t = t.format(self.name,
                     self.count,
                     (min(self.dates)).strftime(ISO_8601),
                     (max(self.dates)).strftime(ISO_8601),
                     (max(self.dates) - min(self.dates)).days)
        return t

    def __init__(self, category, name):
        self.name = name
        self.thedir = os.path.join(category, name)
        self.files = self.file_list(self.thedir)
        self.spectra = [Spectrum(self.thedir, file) for file in self.files]

        self.count = len(self.files)
        self.load_spectra()
        self.max_date = max(self.dates)
        # take first  ra, dec from all spectra
        self.ra = self.spectra[0].ra
        self.dec = self.spectra[0].dec

        print sep1
        print "Added star {} with {} members, max date = {}, ra = {} {}, da = {} {}".format(self.name,
                                                                                      self.count,
                                                                                      self.max_date,
                                                                                      self.ra,
                                                                                      self.ra2deg(self.ra),
                                                                                      self.dec,
                                                                                      self.dec2deg(self.dec))
        
        



class Spectrum(list):
    def read_spectrum(self):
        hdu = pf.open(self.thefile)
        data = hdu[1].data
        self.hdr = hdu[0].header
        self.date = parser.parse(self.hdr['DATE-OBS'])
        self.ra = self.hdr['RA']
        self.dec = self.hdr['DEC']
        hdu.close()
        self.x = data.field('WAVE')
        self.y = data.field('FLUX')
        self.data = True

    def __init__(self, path, name):
        self.name = name
        self.thefile = os.path.join(path, name)
        self.data = False

    def get_header(self, limit):
        l = list(self.hdr)[:limit]
        s = ''
        for i in l:
            s += (i + ' = ' + str(self.hdr[i]))[:40] + '\n'

        return s

if __name__ == '__main__':
    main()
