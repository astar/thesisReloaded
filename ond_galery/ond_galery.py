import os
import math
import sys
import pyfits as pf
import dateutil as dt
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

def main():
    """
    """
    cat = Category('trainning3/9')
    Plot(cat)
    
class Plot():
    def update(self, val):
        frame = numpy.floor(sframe.val)
        ln.set_xdata(xdata[frame])
        ln.set_ydata((frame+1)* ydata[frame])
        ax.set_title(frame)
        ax.relim()
        ax.autoscale_view()
        plt.draw()

    def init_graphs(self):
        self.ln = []
        for ax in self.axes.flat:
            l, = ax.plot([],[])
            ax.autoscale(True)
            self.ln.append(l)

    def populate_frame(self, val):
        """
        """
        # computer lower and upper limit per frame
        lower = (self.frame - 1) * self.graphs
        upper = lower + self.graphs - 1

        text = 'Category {} with {} spectra. Page {}/{}'.format(self.category.name, self.category.count, self.frame, self.frames)
        self.fig.text(0.5,0.975, text, horizontalalignment = 'center', verticalalignment = 'top')

        #import ipdb; ipdb.set_trace()

        index = lower
        for l, ax in zip(self.ln, self.axes.flat):
            if index < upper:
                star = self.category.stars[index]

                # ln, = ax.plot([], [])
                # ln.set_xdata = star.spectra[0].x
                # ln.set_ydata = star.spectra[0].y
                l.set_xdata(star.spectra[0].x)
                l.set_ydata(star.spectra[0].y)

                ax.set_title(star.name)
                ax.title.set_visible(True)
                
            else:
                # hide not used subplots
                ax.set_visible(False)
                
            #some settings
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            index += 1
            
            ax.relim()
            ax.autoscale_view()
            plt.draw()
        
    def __init__(self, category):
        self.category = category
        self.columns = 4
        self.rows = 5
        self.graphs = self.columns * self.rows
        self.frame = 1
        self.frames = int(math.ceil(category.count / float(self.graphs)))
        #ax = [plt.subplot(self.rows, self.columns, actual) for actual in arange(category.count)]
        self.fig, self.axes = plt.subplots(self.rows, self.columns)
        self.fig.subplots_adjust(wspace=0,hspace=0)
        self.init_graphs()
        self.populate_frame(1)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        # buttons
        self.axprev = plt.axes([0.125, 0.03, 0.1, 0.055])
        self.axnext = plt.axes([0.225, 0.03, 0.1, 0.055])
        self.axexit = plt.axes([0.335, 0.03, 0.1, 0.055])
        self.bnext = widgets.Button(self.axnext, '>>')
        self.bnext.on_clicked(self.next)
        self.bprev = widgets.Button(self.axprev, '<<')
        self.bprev.on_clicked(self.prev)
        self.bexit = widgets.Button(self.axexit, '(o)(o)')
        self.bexit.on_clicked(sys.exit)
        
        plt.show()
        
    def next(self, event):
        """
        """
        if self.frame < self.frames:
            self.frame +=1
            self.populate_frame(self.frame)
        
    def prev(self, event):
        """
        """
        if self.frame > 1:
            self.frame -=1
            self.populate_frame(self.frame)
        
    def on_click(self, event):
        """Enlarge or restore the selected axis."""
        ax = event.inaxes

        if ax is None:
            # Occurs when a region not in an axis is clicked...
            return
        if event.button is 1 and ax.has_data():
            # On left click, zoom the selected axes
            ax._orig_position = ax.get_position()
            ax.set_position([0.1, 0.1, 0.85, 0.85])
            for axis in event.canvas.figure.axes:
                # Hide all the other axes...
                if axis is not ax:
                    axis.set_visible(False)
        elif event.button is 3:
            # On right click, restore the axes
            try:
                ax.set_position(ax._orig_position)
                for axis in event.canvas.figure.axes:
                    axis.set_visible(True)
            except AttributeError:
                # If we haven't zoomed, ignore...
                pass
        else:
            # No need to re-draw the canvas if it's not a left or right click
            return
        event.canvas.draw()

class Category(list):
    
    def dir_list(self, thedir):
        return [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
    
    def __init__(self, cat_path):
        self.name = os.path.basename(cat_path)
        self.dirs = self.dir_list(cat_path)
        self.stars = [Star(cat_path, star) for star in self.dirs]
        self.count = len(self.stars)
        print "Added category {} with {} members".format(self.name, self.count)
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
        print "\t Added star {} with {} members".format(self.name, self.count)
        self.preview()


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

if __name__ == '__main__':
    main()