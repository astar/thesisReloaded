#!/bin/sh
# create plots of spectra


for i in * ; do
  if [ -d "$i" ]; then
    python makeSAMPHtml.py "$i/*_detail.png" 
  fi
done
