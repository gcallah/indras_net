#!/bin/sh

export wd=`pwd`
echo "PYTHONPATH=$wd:$PYTHONPATH" >> $HOME/$1
pip3 install -r docker/requirements-dev.txt
