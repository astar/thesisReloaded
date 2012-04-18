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
import sys
import re

class Spectra():
    """ manipulate spectra """

    def __init__(self):
        self.stars = ['a', 'b', 'c', 'd', 'e']


        self.position = 0
        self.get_spectra()
        self.current = self.spectrum[self.position]

    def next(self):
        if self.position < len(self.stars) - 1:
            self.position += 1
            self.current = self.spectrum[self.position]

    def previous(self):
        if self.position > 0:
            self.position -= 1
            self.current = self.spectrum[self.position]

    def get_spectra(self):
        self.spectrum = []
        for i, star in enumerate(self.stars):
            # test data
            x = np.arange(10)
            y = x**i
            self.spectrum.append(Spectrum(star, i, i+1, x, y))

    def open_file(self, name):
        try:
            f = open(name, "r+")
            text = f.read()
            f.close()
            return text
        except IOError:
            print "Could not open file!"

    def parse_fits(self, text):
        """ extract file names form votable """
        fits = re.findall(
            'http://ssaproxy.asu.cas.cz/getproduct/ccd700/data/.{,30}fits', text)
        return fits

class Spectrum():
    """ individual spectrum of a star """
    def __init__(self, name='', ra=0, dec=0, x=[], y=[]):
        self.name = name
        self.ra = ra
        self.dec = dec
        self.x = x
        self.y = y


class Plot():
    def __init__(self, spectra):
        self.spectra = spectra
        self.fig = plt.figure()
        self.connection_id = self.fig.canvas.mpl_connect(
            'button_press_event', self.onclick)
        self.click()

    def plot(self, x, y, info):
        plt.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(x,y)
        plt.show()

    def onclick(self, event):
        if event.button == 1:
            self.spectra.next()
        elif event.button == 2:
            sys.exit(0)
        if event.button == 3:
            self.spectra.previous()

        self.click()

    def click(self):

        # test data
        self.name = self.spectra.current.name
        self.x = self.spectra.current.x
        self.y = self.spectra.current.y
        self.info = ['name', 'ra = 100', 'dec = 200']
        print self.name, self.x, self.y
        self.plot(self.x, self.y, self.info)

class TestClass:
    my_spectra = Spectra()
    test_file = 'votable.xml'
    def test_open_file(self):
        assert self.my_spectra.open_file(self.test_file)

    def test_parse_fits(self):
        text = self.my_spectra.open_file(self.test_file)
        fits = self.my_spectra.parse_fits(text)
        assert len(fits) == 265


def main():

    my_spectra = Spectra()
    my_plot = Plot(my_spectra)

    my_plot.test()




if __name__=='__main__':
    main()