#!/bin/sh

#
# Wrapper script to go from a tsv to features
#

# input tsv file
export tsv_in=$1

# k value
export k_val=$2

# sequences file
export seq_file=${tsv_in}.seqs.txt

# features output file
export features_out=${tsv_in}.features.tsv

# kmer list file
export kmer_list=${tsv_in}.kmer_list.txt

# sorted kmer list file
export sort_kmer_list=${tsv_in}.sorted_kmer_list.txt

# random control sequences file
export random_seqs=${tsv_in}.random_seqs.txt

# random control sequences features file
export random_features_out=${tsv_in}.random_features.tsv


#
# Get the sequences from the tsv file
#
cat $tsv_in | cut -f4 > $seq_file


#
# Write kmers to the kmer file
#
./get_all_kmers.py --inputSeqs $seq_file --kmerList $kmer_list --k $k_val


#
# Sort the kmer file by unique kmer counts
#
cat $kmer_list | sort | uniq -c | sort -rn | awk '{print $2}' | head -n 200 > $sort_kmer_list


#
# Write the feature matrix
#
./sortedKmers_to_features.py --inputSeqs $seq_file --kmerList $sort_kmer_list --outputTSV $features_out


#
# Get the random sequences
#
./generate_random_seqs.py --inputSeqs $seq_file --outputSeqs $random_seqs


#
# Create features for the random sequences
#
./sortedKmers_to_features.py --inputSeqs $random_seqs --kmerList $sort_kmer_list --outputTSV $random_features_out

