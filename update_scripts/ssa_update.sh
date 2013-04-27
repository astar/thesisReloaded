#!/bin/sh
# update fits and summary csv for whole training set


rm -f statistics.csv

for i in * ; do
  if [ -d "$i" ]; then
    python ssa_update.py -s "$i" -u skoda -p vo
  fi
done
