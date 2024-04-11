#!/bin/bash

algos=("glcache")

cache_sizes=("16gb")

retrain_time=43200

log_file="../retrain_time_lab/output_log_$retrain_time.txt"

for alg in "${algos[@]}"
do
    for size in "${cache_sizes[@]}"
    do
        echo "Running prog with algorithm $alg and cache size $size with retrain time of $retrain_time"
        ../_build/cachesim ../data/wiki2018_300m.txt csv $alg $size --num-req=100000000 -t "time-col=1, obj-id-col=2, obj-size-col=3, delimiter= , has-header=false" >> "$log_file"
        ../_build/cachesim ../data/wiki2019_300m.txt csv $alg $size --num-req=100000000 -t "time-col=1, obj-id-col=2, obj-size-col=3, delimiter= , has-header=false" >> "$log_file"
    done
done