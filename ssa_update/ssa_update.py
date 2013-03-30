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
import os
import sys
import pyfits as pf
from dateutil import parser
import datetime as dt
import string
import urllib
import urllib2
from astropy.io.votable import parse_single_table
from cStringIO import StringIO
from optparse import OptionParser

# config
sep1 = 40*'-'
sep2 = 40*'='
sep3 = 40*'*'
ISO_8601 = '%Y-%m-%d'
h_alpha = 6563


# ssa = 'http://skoda:vo@ssaproxy.asu.cas.cz/ccd700/q/pssa/ssap.xml'\
ssa = 'http://ssaproxy.asu.cas.cz/ccd700/q/pssa/ssap.xml'\
      '?POS={},{}&SIZE=0.1&REQUEST=queryData&FLUXCALIB=normalized' \
      '&BAND=6200e-10/6800e-10&format=fits&TIME={}/'


def main():

    prg = os.path.basename(sys.argv[0])
    usage = prg + ' [ <OPTIONS> ] <ARGS>'

    #
    # parse command line, result is stored to 'opts'
    #
    parser = OptionParser(usage, version='%s version 0.1' % prg)

    parser.add_option(
        '-s', '--source-directory', action='store', dest='source_dir',
        default=None, help='specify input directory')
    parser.add_option('-d', '--download', action='store_true', dest='download',
                      default=True, help='specify if fits should be updated')

    parser.add_option('-u', '--user', action='store', dest='user',
                      default=None, help='user name for secure server')

    parser.add_option('-p', '--pass', action='store', dest='password',
                      default=None, help='password')

    opts, args = parser.parse_args()

    source_dir = opts.source_dir
    Opt.download = opts.download
    Opt.user = opts.user
    Opt.password = opts.password
    #
    # chek input parameters
    #
    if not source_dir:
        sys.stderr.write("Wrong --source-directory '%s'\n" % opts.source_dir)
        sys.exit(1)

    #
    # Main logic
    #

    Category(source_dir)


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

    def __repr__(self):
        return str(self.name)
    __str__ = __repr__


class Star(list):

    def download_spectra(self, urls, names):
        """download new spectra into star directory."""
        for url, name in zip(urls, names):
            full_name = os.path.join(self.thedir, name)
            # change .fit to .fits because its in votable
            full_name = full_name.replace('.fit', '.fits')
            if Opt.user and Opt.password:
                url = url.replace('http://', 'http://{}:{}@'.format(
                    Opt.user, Opt.password))
            try:
                urllib.urlretrieve(url, full_name)
            except Exception, e:
                raise e
            finally:
                print '\tfile: {} downloaded into: {}'.format(name,
                                                              self.thedir)

    def parse_votable(self, text):
        """extract file names form votable."""

        _file = StringIO(text)  # create file for parse_single_table func
        _table = parse_single_table(_file, pedantic=False)
        _date = (_table.array['ssa_dateObs']).data
        _url = (_table.array['accref']).data
        _name = (_table.array['ssa_dstitle']).data
        return _date, _url, _name

    def get_ssa(self):
        """download votable of newer fits than stored."""
#        import ipdb; ipdb.set_trace()
        url = ssa.format(self.ra2deg(self.ra),
                         self.dec2deg(self.dec),
                         self.max_date.isoformat())
#        print url
#        import ipdb; ipdb.set_trace()
        try:
            s = urllib2.urlopen(url)
            return s.read()

        except:
            print 'Could not download file'

#        finally:
#            s.close()

    def dec2deg(self, dec):
        """converts dec to degrees."""
        dec = string.split(dec, ':')
        hh = abs(float(dec[0]))
        mm = float(dec[1])/60
        ss = float(dec[2])/3600
        deg = str(hh+mm+ss)
        if float(dec[0]) < 0:
                deg = '-' + deg
        return deg

    def ra2deg(self, ra):
        """converts ra to degrees."""
        ra = string.split(ra, ':')
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
        t = ' Star: {}\n Count: {}\n First: {}\n Last: {}\n Diff: {} days\n'
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
        # add second to get next spectrum
        self.max_date += dt.timedelta(seconds=1)
        # take first  ra, dec from all spectra
        self.ra = self.spectra[0].ra
        self.dec = self.spectra[0].dec
#        import ipdb; ipdb.set_trace()
        votable = self.get_ssa()
        dates, urls, names = self.parse_votable(votable)
        print sep2
        print 'Star: {}\n\t{} spectra\n\tmax date: {}\n'\
              '\tra: {} {} \n\tdec: {} {}'.format(self.name,
                                                  self.count,
                                                  self.max_date,
                                                  self.ra,
                                                  self.ra2deg(
                                                  self.ra),
                                                  self.dec,
                                                  self.dec2deg(self.dec))
        print sep1
        print 'Number of fits to update: {}'.format(len(names))
        print sep1

        if Opt.download:
            self.download_spectra(urls, names)


class Spectrum(list):
    def read_spectrum(self):
        hdu = pf.open(self.thefile)
        data = hdu[1].data
        self.hdr = hdu[0].header
        _date = parser.parse(self.hdr['DATE-OBS'])
        _time = self.hdr['UT']
        h, m, s = map(int, _time.split(':'))
        _time = dt.time(h, m, s)
        self.date = dt.datetime.combine(_date, _time)
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


class Opt(object):
    """General options."""

if __name__ == '__main__':
    main()
