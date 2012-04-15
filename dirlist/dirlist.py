#!/usr/bin/python
""" print number of file in subdirectories """

import sys,os, glob

ext = "fits"
sep = ','

def main():

    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        sys.exit(1)

    dirs = listdir(os.path.join(root,'*'))

    for dir in dirs:
        n = numberOfFiles(os.path.join(os.path.join(dir,'*.' + ext)))
        if n > 0:
            dirNames =  dir.split('/')
            print ("%s%s%s" % (dirNames[0] + sep, dirNames[1] + sep, str(n)))

def listdir(d):
    return glob.glob(d)

def numberOfFiles(d):
    return len(glob.glob(d))


if __name__ == "__main__":
    main()
