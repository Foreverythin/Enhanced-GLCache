#!/bin/bash

algos=("lru" "lfu" "fifo" "clock" "2q" "lecar" "cacheus" "lhd" "glcache")

cache_sizes=("4gb" "16gb")

# retrain_time=43200

log_file="./output_log_wiki2018.txt"

for alg in "${algos[@]}"
do
    for size in "${cache_sizes[@]}"
    do
        echo "Running prog with algorithm $alg and cache size $size"
        ../_build/cachesim ../data/wiki2018_300m.txt csv $alg $size --report-interval 864000000000 -t "time-col=1, obj-id-col=2, obj-size-col=3, delimiter= , has-header=false" >> "$log_file"
        # ../_build/cachesim ../data/wiki2019_300m.txt csv $alg $size -t "time-col=1, obj-id-col=2, obj-size-col=3, delimiter= , has-header=false" >> "$log_file"
    done
done