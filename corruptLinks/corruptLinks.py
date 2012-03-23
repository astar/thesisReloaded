#!/usr/bin/python
import sys, numpy as np, os, glob, re

def main():

    if len(sys.argv) > 1:
        src = sys.argv[1]
    else:
        sys.exit(1)
    
    nFiles, srcs = listdir(src)
    
    for file in srcs:
        data = readFile(file)
        srcDest = map(getNames, data)
        map(makeLink, srcDest)


def makeLink(srcDest):
    if not os.path.islink(srcDest[1]):
        src = os.path.join('..', srcDest[0])
        dest = os.path.join('..','corrupt',srcDest[1])
        os.symlink(src, dest)
    

def getNames(name):
    src = re.sub('\.\./','', name)
    dest = re.sub('/','_',src)
    return [src, dest]

def readFile(file):
    data = np.genfromtxt(file, dtype=None, delimiter=',', names=None)
    #return only spectra which are not fully corrupted
    return data[data['f6'] != 0]['f0']

def listdir(d):
    return len(glob.glob(d)), glob.glob(d)


if __name__ == "__main__":
    main()
