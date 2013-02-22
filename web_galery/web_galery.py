import os
import math
import sys
import pyfits as pf
import dateutil as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.widgets as widgets
sep1 = 40*'-'
sep2 = 40*'='
sep3 = 40*'*'

def main():
    """
    """
    mpl.rc('xtick', labelsize = 8) 
    mpl.rc('ytick', labelsize = 8)
    
    if len(sys.argv) > 1:
        thedir = sys.argv[1]
    else:
        print 'First agrument is the input dir'
        sys.exit(1)
        
    cat = Category(thedir)
    print cat.stars
    #Plot(cat)

class Category(list):
    
    def dir_list(self, thedir):
        return [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
    
    def __init__(self, cat_path):
        self.thedir = cat_path
        self.name = os.path.basename(cat_path)
        self.dirs = self.dir_list(cat_path)
        self.stars = [Star(cat_path, star) for star in self.dirs]
        self.count = len(self.stars)
        print sep2
#        import ipdb; ipdb.set_trace()
        print "Added category {} with {} members".format(self.name, self.count)
    def __repr__(self):
        return str(self.name)
    __str__ = __repr__

    
class Star(list):
    def preview_plot(self):
        """ Plot spectra of the star
        """
        fig, axes = plt.subplots(2)
        fig.subplots_adjust(wspace=0,hspace=0)
        for ax in axes: 
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

            for sp  in self.spectra:
                l, = ax.plot(sp.x, sp.y)

        #zoom
        axes[1].set_xlim(6563 - 50, 6563 + 50)

#        figure = plt.gcf() # get current figure
#        figure.set_size_inches(2, 1.5)

        plt.savefig(self.name + '_preview.png')
        plt.savefig(self.name + '_preview.svg')


    def detail_plot(self ):
        """
        """
        #ax.set_xlabel("$Wavelenght [\\AA]$")
        #ax.set_ylabel("$Energy [10^{-17} erg/s/cm^2/\\AA]$")
        """ Plot spectra of the star
        """
#        fig, axes = plt.subplots(2)
        
#        fig.subplots_adjust(wspace=0,hspace=0)
        axes = []
        axes.append(plt.subplot2grid((2,3), (0,0), colspan = 2))
        axes.append(plt.subplot2grid((2,3), (1,0), colspan = 1))
        axes.append(plt.subplot2grid((2,3), (1,1), colspan = 1))
        info = plt.subplot2grid((2,3), (0,2), rowspan = 2)
        axes[0].separate = False # separate lines
        axes[1].separate = False
        axes[2].separate = True

        
        info.get_xaxis().set_visible(False)
        info.get_yaxis().set_visible(False)
        axes[0].get_xaxis().set_visible(False)
        axes[1].set_xlabel("$Wavelenght [\\AA]$")
#        axes[1].set_ylabel("ADU")
        axes[2].get_yaxis().set_visible(False)
        
        info.text(0.05,0.975, self.statistics(), horizontalalignment = 'left', verticalalignment = 'top', fontsize = 'small')        
        info.text(0.05,0.765, self.spectra[0].get_header(40), horizontalalignment = 'left', verticalalignment = 'top', fontsize = 5)
        
        for ax in axes: 

            for i, sp  in enumerate(self.spectra):
                y = sp.y
                if ax.separate:
                    y = sp.y + i*.07
                l, = ax.plot(sp.x, y)

        #zoom
        axes[1].set_xlim(6563 - 50, 6563 + 50)
        axes[2].set_xlim(6563 - 50, 6563 + 50)

 #       figure = plt.gcf() # get current figure
 #       figure.set_size_inches(8, 6)
        
#        plt.savefig(os.path.join(self.thedir, self.name + '_detail.png'))
        plt.savefig(self.name + '_detail.png')
        plt.savefig(self.name + '_detail.svg')
        

        
#        plt.show()
            
        
    def file_list(self, thedir):
        f = lambda thedir, name: os.path.join(thedir, name) 
        return [ name for name in os.listdir(thedir) if os.path.isfile(f(thedir, name)) and os.path.splitext(f(thedir, name))[1] == '.fits' ]
    

    def load_spectra(self):
        self.dates = []
        for sp in self.spectra:
            sp.read_spectrum()
            self.dates.append(sp.date)
        self.loaded = True
        return True
        
    def statistics(self):
        """
        """
        t = "Star: {} \n #spectra: {} \n first: {} \n last: {} \n diff: {} \n".format( self.name,self.count,min(self.dates), max(self.dates), max(self.dates) - min(self.dates))
        return t
                                
    def __init__(self, category, name):
        self.name = name
        self.thedir = os.path.join(category, name)
        self.files = self.file_list(self.thedir)
        self.spectra = [Spectrum(self.thedir, file) for file in self.files]

        self.count = len(self.files)
        self.load_spectra()
        print sep1
        print "Added star {} with {} members".format(self.name, self.count)
        self.preview_plot()
        self.detail_plot()

class Spectrum(list):
    def read_spectrum(self):
#        print "reading {}".format(self.thefile)
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

    def get_header(self, limit):
        l = list(self.hdr)[:limit]
        s = ''
        for i in l:
            s += (i + ' = ' + str(self.hdr[i]))[:40] + '\n'
            
        return s

if __name__ == '__main__':
    main()