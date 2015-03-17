#! /bin/bash


files=`ls notebooks/*ipynb`
cd docs
for f in $files
do
  b=`basename -s .ipynb $f`
  ipython nbconvert ../notebooks/${b}.ipynb --to rst --output ${b}.rst
done
cd -
