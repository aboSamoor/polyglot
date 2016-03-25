#! /bin/bash

bin='jupyter'
if ! type "$bin" > /dev/null; then
  bin='ipython'
fi

files=`ls notebooks/*ipynb`
cd docs
for f in $files
do
  b=`basename -s .ipynb $f`
  $bin nbconvert ../notebooks/${b}.ipynb --to rst --output ${b}.rst
done
cd -
