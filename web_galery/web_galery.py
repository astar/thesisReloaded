#!/usr/bin/python
import os
import sys
import pyfits as pf
import numpy as np
import dateutil as dt
import matplotlib.pyplot as plt
import matplotlib as mpl

# config
sep1 = 40*'-'
sep2 = 40*'='
sep3 = 40*'*'
ISO_8601 = '%Y-%m-%d'
h_alpha = 6563


def main():
    mpl.rc('xtick', labelsize=8)
    mpl.rc('ytick', labelsize=8)

    if len(sys.argv) > 1:
        thedir = sys.argv[1]
    else:
        print 'First agrument is the input dir'
        sys.exit(1)

    cat = Category(thedir)
    print cat.stars


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
    def preview_plot(self):
        """ thumbail plot
        """
        fig, axes = plt.subplots(2)
        fig.subplots_adjust(wspace=0, hspace=0)

        for ax in axes:
            for sp in self.spectra:
                l, = ax.plot(sp.x, sp.y)

        # disable x on first
        axes[0].get_xaxis().set_visible(False)

        # zoom
        axes[1].set_xlim(6563 - 50, 6563 + 50)

        plt.savefig(self.name + '_preview.png')
        plt.savefig(self.name + '_preview.svg')

    def detail_plot(self):
        """ detailed subplot
        """

        axes = []
        axes.append(plt.subplot2grid((4, 3), (0, 0), rowspan=2, colspan=2))
        axes.append(plt.subplot2grid((4, 3), (2, 0), rowspan=2, colspan=2))
        axes.append(plt.subplot2grid((4, 3), (1, 2), rowspan=3))
        info = plt.subplot2grid((4, 3), (0, 2))
        axes[0].separate = False  # separate lines
        axes[1].separate = False
        axes[2].separate = True

        info.text(0.05, 0.875,
                  self.statistics(),
                  horizontalalignment='left',
                  verticalalignment='top',
                  fontsize='small')

        for ax in axes:

            for i, sp in enumerate(self.spectra):
                y = sp.y
                if ax.separate:
                    y = sp.y + i*.07
                l, = ax.plot(sp.x, y)

            # H alpha line
            ax.axvline(x=h_alpha, color='r', ls='--')

        # adjust axes
        info.get_xaxis().set_visible(False)
        info.get_yaxis().set_visible(False)
        axes[0].get_xaxis().set_visible(False)
        axes[1].set_xlabel("$Wavelenght [\\AA]$")
        axes[2].get_yaxis().set_visible(False)

        # adjust ticks
        axes[1].get_yaxis().set_ticks(np.arange(0.0, 1.2, 0.2))

        # zoom
        axes[1].set_xlim(6563 - 50, 6563 + 50)
        axes[2].set_xlim(6563 - 50, 6563 + 50)

        plt.savefig(self.name + '_detail.png')
        plt.savefig(self.name + '_detail.svg')

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
        print sep1
        print "Added star {} with {} members".format(self.name, self.count)
        self.preview_plot()
        self.detail_plot()


class Spectrum(list):
    def read_spectrum(self):
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

    def get_header(self, limit):
        l = list(self.hdr)[:limit]
        s = ''
        for i in l:
            s += (i + ' = ' + str(self.hdr[i]))[:40] + '\n'

        return s

if __name__ == '__main__':
    main()
