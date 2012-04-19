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
import matplotlib.widgets as widgets
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
        print 'current %s' % self.current.name
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
#        print self.csv_data
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
            print 'openning file %s' % self.name
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

    def get_votable():
        """ Downlad votable from ssa server """
#http://ssaproxy.stel/ccd700/q/pssa/ssap.xml?POS=279.2347,38.7836&SIZE=0.16&REQUEST=queryData&_TDENC=true&band=6500e-10/6700e-10&format=fits' -O votable.xml

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
#        print self.name
        hdu = pyfits.open(self.name)
        data = hdu[1].data
        self.x = data.field('WAVE')
        self.y = data.field('FLUX')




class Plot():
    def __init__(self, stars):

        self.stars = stars
        self.fig = plt.figure()
        plt.autoscale(enable=True, axis='both', tight=None)
        self.fig.subplots_adjust(left=0.25, bottom=0.25)
#        self.connection_id = self.fig.canvas.mpl_connect(
#            'button_press_event', self.onclick)
        # set the maximum separation to the median of the first star
        self.clear()

        # sep slider
        self.sep_max = round(np.median(self.stars.star[0].spectrum[0].y)*3)
        self.axcolor = 'lightgoldenrodyellow'
        self.axfreq = plt.axes([0.3, 0.1, 0.5, 0.03], axisbg=self.axcolor)
        self.sep = widgets.Slider(self.axfreq, 'Sep', 0.1, 1, valinit=0.2)
        self.sep.on_changed(self.update)


        self.click()

    def update(self, val):
        s = self.sep.val
        self.separate(s)
        plt.draw()


    def plot(self, x, y, info):
        self.ax.plot(x,y)



    def clear(self):
        plt.clf()
        self.ax = self.fig.add_subplot(111)



    def onclick(self, event):
  #      if event.button == 1:
 #           self.stars.next()
#        elif event.button == 2:
#            sys.exit(0)
#        if event.button == 3:
#            # self.stars.previous()
#            self.separate()

        self.click()

    def click(self):

        self.name = self.stars.current.name
        self.ra = self.stars.current.ra
        self.dec = self.stars.current.dec
        self.info = ['name', 'ra = 100', 'dec = 200']


        for i, spectrum in enumerate(self.stars.current.spectrum):
            self.x = spectrum.x
            self.y = spectrum.y
            self.plot(self.x, self.y, self.info)

        self.update(self.sep.val)
        plt.show()

    def separate(self, s):
        """ Separate charts  """
        temp_max = []
        for i, line in enumerate(self.ax.lines):
            line.set_ydata(self.y + i*s*self.sep_max)
            temp_max.append(np.max(line.get_ydata()))


        self.ax.set_ylim([0,np.max(temp_max)])

        plt.draw()





class TestClass():
    def __init__():
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

#    my_plot.test()

    # draw the current state (relative to the last reference)




if __name__=='__main__':
    main()