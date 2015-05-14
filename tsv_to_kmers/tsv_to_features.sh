#!/bin/sh

#
# Wrapper script to go from a tsv to features
#

# input uniprot tsv file
export uniprot_tsv=$1

# k value
export k_val=$2

# directory to store features and intermediate files
export ft_dir=$3

#
# Iterate through all annotations we want to use
#

for annot in helix turn transmembrane-region strand nucleotide-phosphate-binding-region
do

  echo 'running tsv_to_features.sh for' $annot

  # feature basename
  export ft_basepath=${ft_dir}/${annot}

  # extracted feature tsv file
  export tsv_in=${ft_basepath}.tsv

  # extracted sequences file
  export seq_file=${ft_basepath}.seqs.txt

  # features output file
  export features_out=${ft_basepath}.features.tsv

  # kmer list file
  export kmer_list=${ft_basepath}.kmer_list.txt

  # sorted kmer list file
  export sort_kmer_list=${ft_basepath}.sorted_kmer_list.txt

  # random control sequences file
  export random_seqs=${ft_basepath}.random_seqs.txt

  # random control sequences features file
  export random_features_out=${ft_basepath}.random_features.tsv


  #
  # Extract this annotation from the uniprot tsv file
  #
  #
  ./process_tsv.py --inputTSV $uniprot_tsv --outputTSV $tsv_in


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

done
