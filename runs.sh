#!/bin/bash

num_runs=$1
run_file=$2
props=$3
data_base=$4
periods=$5

for ((i=1;i <= num_runs; i++))
do
    datafile="$data_base.$i.csv"
    python $run_file $props -periods $periods -datafile $datafile > /dev/null
done
