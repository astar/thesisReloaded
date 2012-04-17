#!/usr/bin/env python
# -*- coding: ascii -*-

"""
ema (emission manual analyzer)
- read name,ra,dec from csv file
- download spectra from server
- shows them in one plot
- store selected object in a file

"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 2009-2010 Joe Author'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/

import Tkinter as tki

def main():
    while True:
        key = raw_input('Input:')
        if key == ' ':
            print 'next'
        elif key.lower() == 'a':
            print 'add'
        else:
            print 'Press a for add or SPC for next'


if __name__=='__main__':
    main()