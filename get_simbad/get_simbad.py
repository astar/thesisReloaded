#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module Docstring
open list of stars
get hd name, ra, dec, fluxes from simbad
"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 2009-2010 Joe Author'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/

#
## Code goes here.
#
from coatpy import  Sesame
from BeautifulSoup import BeautifulSoup
import re

def get_simbad(name):
    """
    """
    web_name = name.replace(' ','%20')
    simbad = Sesame(opt='S', opt1 ='oxif')
    xml = simbad.resolveRaw(web_name)
    tree = BeautifulSoup(xml)

    if no_data(tree):
        print name
        return False

    star_info = parse_flux(tree)
    ra, dec = parse_radec(tree)
    hd_name = parse_hd_name(tree)

#    import ipdb;ipdb.set_trace()
    star_info['CAT-RA'] = ra
    star_info['CAT-DEC'] = dec
    star_info['hd_name'] = hd_name
    star_info['name'] = name

    return star_info

def no_data(tree):
    """ check if simbad return data
    """
    try:
        info = tree.find("info").string
    except:
        return False

    if re.search("Nothing found", info):
        return True

    return False

def parse_radec(tree):
    """
    """
    try:
        ra = tree.find("jradeg").string
        dec = tree.find("jdedeg").string
    except:
        return None, None
    return  ra, dec

def parse_flux(tree):
    """
    """
    fluxes = {}
    tags = tree.findAll("mag")
    for tag in tags:
#        import ipdb;ipdb.set_trace()
        fluxes[tag['band']] = tag.findChild("v").string
    return fluxes

def parse_hd_name(tree):
    """ Extract HD name from tree
    """
    hd = [alias.string for alias in tree.findAll("alias") if re.search("HD.*", alias.string) ]
    if not hd:
        return None
    return hd.pop()

if __name__=='__main__':
    main()
