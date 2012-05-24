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
            star_tmp = Star(name, ra, dec)
            self.star.append(star_tmp)
            print 'added star: {}'.format(name)


            

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
            print "Could not open file {}!".format(self.name)

    def open_csv(self):
        try:
            f = csv.reader(open(self.name, "rU"))
            data = []
            data.extend(f)
            return data

        except IOError:
            print "Could not open file!"

    def append(self, line):
        try:
            f = open(self.name, "a")
            f.write(line + '\n')
            return True

        except IOError:
            print "Could append to file!"

    def move(self, dest):
        try:          
            s.move(self.name, dest)
            return True

        except IOError:
            print "Could not move  file to dir!"
    
    def remove(self):
        try:
            if os.path.isfile(self.name):
                os.remove(self.name)
            return True
        except IOError:
            print "Could not remove file!"

    def remove_pattern(self):
        try:
            for f in os.listdir('.'):
                if re.search(self.name, f):
                    os.remove(f)
                    print 'removing {}'.format(f)
            return True
        except IOError:
            print "Could not remove file!"

    def download(self, url):
        try:
            s = urllib2.urlopen(url)
            content = s.read()
            s.close()
            d = open(self.name,'w')
            d.write(content)
            d.close()
        except IOError:
            print "Could not download file" 




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
class Init():
    """ Clean working direcory and prepare categories """
    def __init__(self):
        self.file = File('categories.txt')
        self.xml  = File('.*.xml')
        self.file.remove()
        self.xml.remove_pattern()
        self.category = ['1', '2', '3', '4', '5', '6', '7']
        for c in self.category:
            self.cat_dir = Dir(c)
            self.cat_dir.remove()
            self.cat_dir.create()

class Category():
    """ Manipulate category of the spectra, create, move """
    def __init__(self, files, star, name):
        self.name = name
        self.star = star
        self.files = files

    def move(self, category):
        """ move star to category """
        for f in self.files:
            spectrum_file = File(f)
            star_dir = Dir(os.path.join(category, self.star))
            star_dir.create()
            cat_path = os.path.join(category, self.star)
            cat_path = os.path.join(cat_path, os.path.basename(f))
            spectrum_file.move(cat_path)
        
        print 'star {} moved into category {}'.format(self.star, category)

        self.cat_file = File('categories.txt')
        self.cat_file.append(self.star + '\t' + category)

         
class Star():
    """  """

    def __init__(self, name, ra, dec):
        self.file_name = name + '.xml'
        star_file = File(self.file_name)
        self.name = name
        self.ra = ra
        self.dec = dec
        self.get_votable(ra, dec) 
        self.file_text = star_file.open_file()
        self.files = self.parse_votable(self.file_text)
        if self.files:
            self.get_spectra()
            self.category = Category(self.download_names, self.name, 'None')



    def download_spectra(self, dir, files):
        self.my_dir = Dir(os.path.join(dir,self.name))
        self.my_dir.remove() # delete temp dir for download with old files
        self.my_dir.create() # create new one
        self.download_names = []

        for url in files:
            file_name = url.split('/').pop() #last part
            file_name = file_name.split('?')[0] # just *.fits
            download_name = os.path.join(dir, self.name)
            download_name = os.path.join(download_name, file_name)

#            print url
            try:
                    s = urllib2.urlopen(url)
                    content = s.read()
                    s.close()
                    d = open(download_name,'w')
                    d.write(content)
                    d.close()
                    self.download_names.append(download_name)

            except IOError:
                print "Could not download file %s!" % url
                pass

    def get_spectra(self):
        self.download_spectra('download', self.files)
        self.spectrum = []
        for f in self.download_names:
            self.spectrum.append(Spectrum(f))

    def get_votable(self, ra, dec):
        """ Downlad votable from ssa server """
        url = 'http://ssaproxy.asu.cas.cz/ccd700/q/pssa/ssap.xml?POS={},{}&SIZE=0.16&REQUEST=queryData&_TDENC=true&band=6500e-10/6700e-10&format=fits'
        url = url.format(float(ra)*15, dec)
        print ra, dec, url
        url_file = File(self.file_name)
        url_file.download(url)

    def parse_votable(self, text):
        """ extract file names form votable """
        try:
            fits = re.findall(
        'http://ssaproxy.asu.cas.cz/getproduct/ccd700/data/.{,40}fits[^<]{,50}',
            text)
            return fits
        except:
            print "Cannot read votable"



class Spectrum():
    """ individual spectrum of a star """
    def __init__(self, name):
        self.name = name
        self.load()

    def load(self):
#        print self.name
        hdu = pyfits.open(self.name)
        data = hdu[1].data
        hdu.close()
        self.x = data.field('WAVE')
        self.y = data.field('FLUX')




class Plot():
    def __init__(self, stars):

        self.stars = stars
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('key_press_event', self.move_into_category)
        plt.autoscale(enable=True, axis='both', tight=None)
        self.fig.subplots_adjust(left=0.25, bottom=0.25)
        self.click()
        #        self.connection_id = self.fig.canvas.mpl_connect(
#            'button_press_event', self.onclick)
        # set the maximum separation to the median of the first star
#        self.clear()

    def show_buttons(self):
        # sep slider
        self.sep_max = round(np.median(self.stars.star[0].spectrum[0].y)*3)
        self.axcolor = 'lightgoldenrodyellow'
        self.axfreq = plt.axes([0.3, 0.1, 0.5, 0.03], axisbg=self.axcolor)
        self.sep = widgets.Slider(self.axfreq, 'Sep', 0.1, 1, valinit=0.2)
        self.sep.on_changed(self.update)

        # buttons
        self.axprev = plt.axes([0.49, 0.03, 0.1, 0.055])
        self.axnext = plt.axes([0.59, 0.03, 0.1, 0.055])
        self.axexit = plt.axes([0.70, 0.03, 0.1, 0.055])
        self.bnext = widgets.Button(self.axnext, 'Next')
        self.bnext.on_clicked(self.nex)
        self.bprev = widgets.Button(self.axprev, 'Previous')
        self.bprev.on_clicked(self.prev)
        self.bexit = widgets.Button(self.axexit, 'Exit')
        self.bexit.on_clicked(sys.exit)

    def move_into_category(self, event):
        """ call function to move spectrum into category """

        if event.key in ['1', '2', '3', '4', '5', '6', '7']:
            print event.key
            self.stars.current.category.move(event.key)
            self.fig.savefig(os.path.join(event.key, self.stars.current.name) + '.png')
            self.nex(1) # go to next star after moving current to category
            
        else:
            print 'This category is no defined'


            
    def show_legend(self):
        legend = 'Star: ' + self.name + '\n' + 'RA: ' + \
        self.ra + '\n' + 'DEC: ' + self.dec + '\n' + 'spectra: ' + self.number_of_spec 
        plt.text(-6.5, 16, legend, fontsize=14, ha='left', va='top')


    def nex(self, event):
        self.stars.next()
        self.click()

        
    def prev(self, event):
        self.stars.previous()
        self.click()

        
    def update(self, val):
        s = self.sep.val
        self.separate(s)



    def plot(self, x, y):

        self.ax.plot(x,y)
        self.ax.set_xlabel("$Wavelenght [\\AA]$")
        self.ax.set_ylabel("ADU")
        #self.ax.axvline( x = 6563, y = 1, color = 'g', ls ='--')
        
        

    def clear(self):
        plt.clf()
        self.ax = self.fig.add_subplot(111)



  #  def onclick(self, event):
  #      if event.button == 1:
 #           self.stars.next()
#        elif event.button == 2:
#            sys.exit(0)
#        if event.button == 3:
#            # self.stars.previous()
#            self.separate()

#        self.click()

    def click(self):
        self.clear()

        self.name = self.stars.current.name
        self.ra = self.stars.current.ra
        self.dec = self.stars.current.dec
        self.number_of_spec = str(len(self.stars.current.files))
        print 'current %s' % self.name

        self.show_buttons()
        self.show_legend()

        
        for i, spectrum in enumerate(self.stars.current.spectrum):
            self.x = spectrum.x
            self.y = spectrum.y
            self.plot(self.x, self.y)

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
    
    Init()
    my_stars = Stars('stars.csv')
    my_plot = Plot(my_stars)

#    my_plot.test()

    # draw the current state (relative to the last reference)




if __name__=='__main__':
    main()
