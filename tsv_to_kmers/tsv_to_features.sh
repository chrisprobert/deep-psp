#!/bin/sh

#
# Wrapper script to go from a tsv to features
#

# input tsv file
export tsv_in=$1

# k value
export k_val=$2

# number of features
export num_fts=$3

# features output file
export features_out=${tsv_in}.features.tsv

# kmer list file
export kmer_list=${tsv_in}.kmer_list.txt


#
# Write kmers to the kmer file
#
./get_all_kmers.py --inputTSV $tsv_in --kmerList $kmer_list --k $k_val


#
# Process the kmer file
#
cat $kmer_list | sort | uniq -c | sort -rn | awk '{print $2}' | head -n${num_conts}


#
# Write the feature matrix
#
./sortedKmers_to_features.py --inputTSV $tsv_in --kmerList $kmer_list --outputTSV $features_out --k $k_val
