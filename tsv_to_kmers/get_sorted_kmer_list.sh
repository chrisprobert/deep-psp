#!/bin/sh

#
# Simple bash script to sort a kmer list
#


# input kmer list file
export kmer_list=$1
export num_conts=$2

# run sorting command
cat $kmer_list | sort | uniq -c | sort -rn | awk '{print $2}' | head -n $num_conts

