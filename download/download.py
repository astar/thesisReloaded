#!/usr/bin/python
import urllib as u, urllib2,  numpy as np, time
from os.path import basename
from urlparse import urlsplit

''' Load file download.sh '''
''' extract url and file name '''
''' Download file   '''
''' 3 alternative downloads are tested here '''

''' file format '''
''' wget "http://data.sdss3.org/returnSpec/fits?plateid=1880&mjd=53262&fiber=1" -O 2116692154469345280.fits '''
''' wget "http://data.sdss3.org/returnSpec/fits?plateid=1880&mjd=53262&fiber=2" -O 2116692429347252224.fits '''

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def ret(list):
    '''Download file from the list'''

    for row in list:
        with Timer() as t:
            download3(row[1].replace('"',''),row[3])
        print 'Download {0} took {1:.3f} sec.'.format(row[3], t.interval)    



def download(url, name):
    '''download url '''
    u.urlretrieve(url,name)

def url2name(url):
    return basename(urlsplit(url)[2])

def download2(url, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
    if localName[0] == '"' or localName[0] == "'":
        localName = localName[1:-1]
    elif r.url != url: 
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName: 
        # we can force to save the file as specified name
        localName = localFileName
        f = open(localName, 'wb')
        f.write(r.read())
        f.close()


def download3(url, name):
    '''download url '''

    file = urllib2.urlopen(url)
    output = open(name,'wb')
    output.write(file.read())
    output.close()





def load(fileName):
    '''load list of files from file'''
    with Timer() as t: 
        data = open(fileName).read()
        dataList = [line.split(' ') for line in data.split('\n') if line] 
    print 'Load {0} took {1:.3f} sec.'.format(fileName, t.interval)    
    return dataList

if __name__ == '__main__':
    list = load('download.sh') # filename 
    ret(list[0:10]) # specify number of lines from file 
