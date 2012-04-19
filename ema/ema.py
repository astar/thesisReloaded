#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ema (emission manual analyzer)
- read name,ra,dec from csv file
- download spectra from server
- shows them in one plot
- store selected object in a file

"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 20012-3012 Astar'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/


import matplotlib.pyplot as plt
import numpy as np
import shutil as s
import urllib2
import pyfits
import sys
import csv
import re
import os

class Stars():
    """ """

    def __init__(self, file_name):
        self.file_name = file_name
        stars_file = File(self.file_name)
        self.csv_data = stars_file.open_csv()
        self.get_stars()
        self.position = 0
        self.current = self.star[self.position]

    def next(self):
        if self.position < len(self.csv_data) - 1:
            self.position += 1
            self.current = self.star[self.position]

    def previous(self):
        if self.position > 0:
            self.position -= 1
            self.current = self.star[self.position]



    def get_stars(self):
        self.star = []
        for d in self.csv_data:
            name = d[0]
            ra   = d[1]
            dec  = d[2]
            file_name = self.get_file_name()
            self.star.append(Star(file_name, name, ra, dec))

    def get_file_name(self):
        return 'votable.xml'




class File():
    def __init__(self, name):
        self.name = name

    def open_file(self):
        try:
            f = open(self.name, "r+")
            text = f.read()
            f.close()
            return text
        except IOError:
            print "Could not open file!"

    def open_csv(self):
        try:
            f = csv.reader(open(self.name, "rU"))
            data = []
            data.extend(f)
            return data

        except IOError:
            print "Could not open file!"

class Dir():
    def __init__(self, name):
        self.name = name

    def remove(self):
        if  os.path.exists(self.name):
            try:
                s.rmtree(self.name)

            except IOError:
                print "Could not remove dir %s!" % name

    def create(self):
        if not os.path.exists(self.name):
            try:
                os.makedirs(self.name)

            except IOError:
                print "Could not remove dir %s!" % name


class Star():
    """  """

    def __init__(self, file_name, name, ra, dec):
        self.file_name = file_name
        star_file = File(self.file_name)
        self.name = name
        self.ra = ra
        self.dec = dec
        self.file_text = star_file.open_file()
        self.files = self.parse_votable(self.file_text)
        self.get_spectra()


    def download_spectra(self, dir, files):
        self.my_dir = Dir(dir)
        self.my_dir.remove() # delete temp dir for download with old files
        self.my_dir.create() # create new one
        self.download_names = []

        for url in files:
            download_name = url.split('/').pop() #last part
            download_name = download_name.split('?')[0] # just *.fits
            download_name = os.path.join(dir, download_name)
            self.download_names.append(download_name)

            try:
                    s = urllib2.urlopen(url)
                    content = s.read()
                    s.close()
                    d = open(download_name,'w')
                    d.write(content)
                    d.close()
            except IOError:
                print "Could not download file %s!" % f

    def get_spectra(self):

        self.download_spectra('download', self.files)
        self.spectrum = []
        for f in self.download_names:
            self.spectrum.append(Spectrum(f))

    def parse_votable(self, text):
        """ extract file names form votable """
        fits = re.findall(
        'http://ssaproxy.asu.cas.cz/getproduct/ccd700/data/.{,40}fits[^<]{,50}',
            text)
        return fits



class Spectrum():
    """ individual spectrum of a star """
    def __init__(self, name):
        self.name = name
        self.load()

    def load(self):
        print self.name
        hdu = pyfits.open(self.name)
        data = hdu[1].data
        self.x = data.field('WAVE')
        self.y = data.field('FLUX')




class Plot():
    def __init__(self, stars):

        self.stars = stars
        self.fig = plt.figure()
        self.connection_id = self.fig.canvas.mpl_connect(
            'button_press_event', self.onclick)
        self.click()

    def plot(self, x, y, info):
        self.ax.plot(x,y)


    def clear(self):
        plt.clf()
        self.ax = self.fig.add_subplot(111)


    def onclick(self, event):
        if event.button == 1:
            self.stars.next()
        elif event.button == 2:
            sys.exit(0)
        if event.button == 3:
            self.stars.previous()

        self.click()

    def click(self):


        # test data
        self.name = self.stars.current.name
        self.ra = self.stars.current.ra
        self.dec = self.stars.current.dec
        self.info = ['name', 'ra = 100', 'dec = 200']
        print self.name, self.ra, self.dec
        self.clear()

        for spectrum in self.stars.current.spectrum:
            self.x = spectrum.x
            self.y = spectrum.y
            self.plot(self.x, self.y, self.info)
        plt.show()


class TestClass:
    test_file = 'votable.xml'
    my_stars = Stars('stars.csv')
    my_file = File(test_file)
    def test_open_file(self):
        assert self.my_file.open_file()

    def test_parse_votable(self):
        my_star = Star(self.test_file,'kacenka', '10', '20')
        text = self.my_file.open_file()
        fits = my_star.parse_votable(text)
        assert len(fits) == 6
    def tes_dir(self):
        my_dir = Dir('test')
        my_dir.create()
        my_dir.remove()




def main():

    my_stars = Stars('stars.csv')
    my_plot = Plot(my_stars)

    my_plot.test()




if __name__=='__main__':
    main()