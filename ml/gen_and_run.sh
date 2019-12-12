#!/bin/bash
if [ -z $1 ]
then
    echo "Using the default data json file"
    ../run.sh used_cars.py 10_50_data.json
else
    ../run.sh used_cars.py $1
fi
