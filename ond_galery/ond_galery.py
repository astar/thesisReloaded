import os
import math
import sys
import pyfits as pf
import dateutil as dt
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
sep1 = 40*'-'
sep2 = 40*'='
sep3 = 40*'*'

def main():
    """
    """
    cat = Category('trainning3/3')
    Plot(cat)
    
class Plot():
    def init_graphs(self):
        self.ln = []
        self.tx = []
        for ax in self.axes.flat:
            l, = ax.plot([],[])
            ax.autoscale(True)
            self.ln.append(l)
            self.tx.append(ax.text(0.3, 0.9, "", ha = 'center', va = 'center', transform=ax.transAxes, fontsize = 'small'))

        self.title = self.fig.text(0.5,0.975, "", horizontalalignment = 'center', verticalalignment = 'top')

    def populate_frame(self, val):
        """
        """
        # computer lower and upper limit per frame
        lower = (self.frame - 1) * self.graphs
        upper = lower + self.graphs - 1


        #import ipdb; ipdb.set_trace()
        index = lower
        text = 'Category {} with {} spectra. Page {}/{}'.format(self.category.name, self.category.count, self.frame, self.frames)
        self.title.set_text(text)
        
        for t, l, ax in zip(self.tx, self.ln, self.axes.flat):
            if index <= upper and index < len(self.category.stars):
                if index > 170:
                    import ipdb; ipdb.set_trace()
                ax.star = self.category.stars[index]

                l.set_xdata(ax.star.spectra[0].x)
                l.set_ydata(ax.star.spectra[0].y)
                t.set_text(ax.star.name)
                
                
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
        self.focus = False
        self.frames = int(math.ceil(category.count / float(self.graphs)))
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
        if event.button is 1 and ax.has_data() and not self.focus:
            # On left click, zoom the selected axes
            self.focus = True
            ax._orig_position = ax.get_position()
            ax.set_position([0.1, 0.1, 0.85, 0.85])
            # load and plot rest of the spectra
            ax.star.load_spectra()
            ax.star.statistics()
            
            for sp  in ax.star.spectra:
                l, = ax.plot(sp.x, sp.y)

            ax.axes.get_xaxis().set_visible(True)
            ax.axes.get_yaxis().set_visible(True)

            for axis in event.canvas.figure.axes:
                # Hide all the other axes...
                if axis is not ax:
                    axis.set_visible(False)
        elif event.button is 3:
            # On right click, restore the axes
            self.focus = False
            try:
                ax.set_position(ax._orig_position)
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)

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

    def load_spectra(self):
        self.dates = []
        for sp in self.spectra:
            sp.read_spectrum()
            self.dates.append(sp.date)
        
    def statistics(self):
        """
        """
        print sep2
        print "Star: {}".format(self.name)
        print "#spectra: {}".format(self.count)
        print "first: {}".format(min(self.dates))
        print "last: {}".format(max(self.dates))
        print "diff: {}".format(max(self.dates) - min(self.dates))
        print sep2
        
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