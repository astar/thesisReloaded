#!/bin/sh
# create plots of spectra


for i in * ; do
  if [ -d "$i" ]; then
    rm -f $i.html
    python makeHtmlTable.py "$i/*_preview.png" 
  fi
done
