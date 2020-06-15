#!/bin/sh
# sets up a new developer

export wd=`pwd`
echo "export PYTHONPATH=$wd:$PYTHONPATH" >> $HOME/$1
export PYTHONPATH=$wd:$PYTHONPATH
echo "export INDRA_HOME=$wd" >> $HOME/$1
export INDRA_HOME=$wd
pip3 install -r docker/requirements-dev.txt
