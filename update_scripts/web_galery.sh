#!/bin/sh
# create plots of spectra


for i in * ; do
  if [ -d "$i" ]; then
    # remove all previous versions
    for e in *.png *.svg; do
	find $i -name $e -print0 | xargs -0  rm -f
    done
    python web_galery.py "$i" 
  fi
done
