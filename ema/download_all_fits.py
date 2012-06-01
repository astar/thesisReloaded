#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
download all spectra from ond server

"""

__author__ = 'Jaroslav Vazny (jaroslav.vazny@gmail.com)'
__copyright__ = 'Copyright (c) 20012-3012 Astar'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/

import urllib2
import re
import os
from gavo import votable

data, metadata = votable.load('votable.xml')

count = len(data)

for i,d  in enumerate(data):

    url = d[1]
    base_dir = 'all_fits' 
    star_dir = url.split('/')[6]
    dir = os.path.join(base_dir, star_dir)
    name = os.path.basename(d[1])
    name = re.findall('.*.fits',name)
    name = str(name[0])

    try:
        s = urllib2.urlopen(url)
        content = s.read()
        s.close()
#        import ipdb; ipdb.set_trace()
        if not os.path.exists(dir):
            os.makedirs(dir)
        d = open(os.path.join(dir, name),'w')
        d.write(content)
        d.close()
        print 'downloaded: {}/{} file: {}'.format(i, count, name)
    except IOError:
        print "Could not download file %s!" % url
        pass