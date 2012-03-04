#!/usr/bin/python
import sys, pyfits, numpy as np, pylab as p, matplotlib.pyplot as plt, os

#show position of some lines
Halpha = 6564.614
type = 3 # type of the spectrum 1 = ond, 2 = dr7 , 3 = dr8 
save = 0

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    print 'This utility plot fits file passed as argument'
if len(sys.argv) == 3:
    type = int(sys.argv[2])

if len(sys.argv) == 4:
    save = int(sys.argv[3])



print file
print type

def readParam(file, param):
    """ Read fits file. Retrun valeu of parameter """
    hdu = pyfits.open(file)
    value = hdu[0].header[param]
    return value

def read(file,type):
    """ Read fits file. Convert wavelength to angstroms """ 
    if type == 1:
        print file
        hdu = pyfits.open(file)
        data = hdu[1].data
        x = data.field('WAVE')
        y = data.field('FLUX')
        return np.asarray([x, y])

    elif type == 2:
        data = pyfits.getdata(file)
        w = lambda x : 10.0**(3.5796 + x*10.0**(-4))
        x = np.arange(1,data[0].size + 1)
        xx  = w(x) # convert to actual wavelenght
        return np.asarray([xx, data[0]])

    elif type == 3:
        print file
        hdu = pyfits.open(file)
        data = hdu[1].data
        x = data.field('wavelength')
        y = data.field('flux')
        return np.asarray([x, y])

    else:
        print 'Unknown type'

def plot(file,xdata,ydata,spLine):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    graph = ax.plot(xdata,ydata, 'r')
    ax.set_title(file)
    ax.set_xlabel("$Wavelenght [\\AA]$")                                                                            
    ax.set_ylabel("$Energy [10^{-17} erg/s/cm^2/\\AA]$")
    ax.axvline(x=spLine, color = 'g', ls ='--')

    


    fig.savefig(file[:-4] + '.png')
    #spLines
    #ax.annotate(
    #    r'$H_{\alpha}$', xy=(spLine, 200),  xycoords='data',
    #            xytext=(-30, -30), textcoords='offset points',
    #            arrowprops=dict(arrowstyle="->",
    #                            connectionstyle="arc3,rad=.2")
    #            )


    #plt.show()

def plot2(file, spLine, xx,yy):
    """ Plot the result with shared axes"""
    fig = plt.figure()
    nsp = len(xx)
    sp = range(1,nsp+1) # number of subplots
    ax = list()
    for x,y,s in zip(xx,yy,sp):
        subplot = int(str(nsp) + '1' + str(s))
        if s > 2:
            ax.append(fig.add_subplot(subplot, sharex=ax[0],sharey=ax[0] ))
        else:
            ax.append(fig.add_subplot(subplot))
            
        graph = ax[s-1].plot(x,y, 'r')
        ax[s-1].set_xlabel("$Wavelenght [\\AA]$")                                                                          
        ax[s-1].set_ylabel("$Energy [10^{-17} erg/s/cm^2/\\AA]$")
        ax[s-1].axvline(x = spLine, color = 'g', ls ='--')

# ax2 = fig.add_subplot(412 )
# graph2 = ax2.plot(xx,yy, 'r')

# ax2.set_ylabel("$Energy [10^{-17} erg/s/cm^2/\\AA]$")

# ax3 = fig.add_subplot(413,sharex=ax2,sharey=ax2 )
# graph3 = ax3.plot(xxx,yyy, 'r')

# ax4 = fig.add_subplot(414,sharex=ax2,sharey=ax2 )
# graph4 = ax4.plot(xxxx,yyyy, 'r')

# ax3.set_xlabel("$Wavelenght [\\AA]$")
    
    #obj = readParam(file, 'OBJTYPE')    
#    ax[0].set_title(file + ' ' + obj )

    basename = os.path.basename(file)
    ax[0].set_title(basename)
    if save:
        filename = os.path.splitext(basename)[0] + '.svg'
        plt.savefig(filename)
    else:
        plt.draw()
        plt.show()

data = read(file,type)
#plot(file, data[0,:], data[1,:], Halpha)

x = data[0,:]
y = data[1,:]
ra = 50
xr = x[(x < Halpha + ra) & (x > Halpha - ra)]
yr = y[(x < Halpha + ra) & (x > Halpha - ra)]

plot2(file,6563,[x, xr ],[y, yr])


