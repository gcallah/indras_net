#!/bin/bash

if [ -z $1 ]
then
    echo "Must pass name of model to run."
fi

export user_type="terminal"
python3 $1.py
