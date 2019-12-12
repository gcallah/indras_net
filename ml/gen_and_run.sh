#!/bin/bash
if [ -z $1 ]
then
    echo "Using the default data json file"
    export user_type="terminal"
    python3 used_cars.py 10_50_data.py
fi
export user_type="terminal"
python3 used_cars.py $1
