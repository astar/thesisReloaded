#!/bin/sh
# create plots of spectra
echo "doing ssa update"
./ssa_update.sh
echo "doing web galery"
./web_galery.sh
echo "doing preview html pages"
./makeHtmlTable.sh
echo "doing detail html pages"
./makeSAMPHtml.sh
echo "doing statistics pages"
python statistics.py
