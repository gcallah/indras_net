#!/bin/bash

if [ -z $1 ]
then
    echo "Must pass name of model to run."
    exit 1
fi

export user_type="terminal"
python3 $@
