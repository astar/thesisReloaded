#!/bin/sh
# update fits and summary csv for whole tarining set
for i in * ; do
  if [ -d "$i" ]; then
    ssa_update "$i"
  fi
done
