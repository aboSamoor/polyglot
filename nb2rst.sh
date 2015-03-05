#! /bin/bash


for f in `ls notebooks/*ipynb`
do
  b=`basename -s .ipynb $f`
  ipython nbconvert $f --to rst --output docs/${b}.rst
done
