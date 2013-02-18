import os
import math
import pyfits as pf
import dateutil as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

def main():
    """
    """
    cat = Category('trainning3/3')
    Plot(cat)
    
class Plot():

    def __init__(self, category):
        self.columns = 4
        self.rows = int(math.ceil(category.count / float(self.columns)))
        print "plot will be {} x {}".format(self.rows, self.columns)
        #ax = [plt.subplot(self.rows, self.columns, actual) for actual in arange(category.count)]
        fig, axes = plt.subplots(self.rows, self.columns)
        fig.subplots_adjust(wspace=0,hspace=0)
        
        for index, ax in enumerate(axes.flat):
            if len(category.stars) > index:

                star = category.stars[index]
                ax.plot(star.spectra[0].x, star.spectra[0].y)
                ax.set_title = "test"
                ax.title.set_visible(True)
                
            else:
                # hide not used subplots
                ax.set_visible(False)
                
            #some settings
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
        

        plt.show()




class Category(list):
    
    def dir_list(self, thedir):
        return [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
    
    def __init__(self, cat_path):
        self.name = os.path.basename(cat_path)
        self.dirs = self.dir_list(cat_path)
        self.stars = [Star(cat_path, star) for star in self.dirs]
        self.count = len(self.stars)
        print "Added category {} with {} members".format(self.name, self.count)
        print self.stars
    def __repr__(self):
        return str(self.name)
    __str__ = __repr__

class Star(list):
    def file_list(self, thedir):
        f = lambda thedir, name: os.path.join(thedir, name) 
        return [ name for name in os.listdir(thedir) if os.path.isfile(f(thedir, name)) and os.path.splitext(f(thedir, name))[1] == '.fits' ]
    
    def preview(self):
        self.spectra[0].read_spectrum()
    def __init__(self, category, name):
        self.name = name
        self.thedir = os.path.join(category, name)
        self.files = self.file_list(self.thedir)
        self.spectra = [Spectrum(self.thedir, file) for file in self.files]
        self.count = len(self.files)
        print "Added star {} with {} members".format(self.name, self.count)
        self.preview()


class Spectrum(list):
    def read_spectrum(self):
        print "reading {}".format(self.thefile)
        hdu = pf.open(self.thefile)
        data = hdu[1].data
        self.hdr = hdu[0].header
        self.date = dt.parser.parse(self.hdr['DATE-OBS'])
        hdu.close()
        self.x = data.field('WAVE')
        self.y = data.field('FLUX')
        self.data = True
        
    def __init__(self, path, name):
        self.name = name
        self.thefile = os.path.join(path, name)
        self.data = False
        #self.read_spectrum(self.thefile)

if __name__ == '__main__':
    main()