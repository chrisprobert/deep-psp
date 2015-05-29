#!/bin/sh

#
# Create random sequence features. Use both uniprot-wide background,
# and same-context background amino acid distributions.
#

UNIPROT_TSV=../../uniprot_sprot.xml.tsv
OUTPUT_DIR=../../seq_features/
GLOBAL_DISTR=${OUTPUT_DIR}uniprot_seqs.txt


# schema of uniprot TSV file:
# id	seq_feature.type	seq_feature.description	start	stop	seq


# get the background sequence distribution
sed "1d" $UNIPROT_TSV | shuf -n 100000 | awk '{if(length($6) > 9) {print $6}}' | tr '[:lower:]' '[:upper:]' > ${OUTPUT_DIR}all_seqs.txt
fold -w 1 ${OUTPUT_DIR}all_seqs.txt | sort | uniq -c > $GLOBAL_DISTR &


# get background distr per-feature
for feature in chain transmembrane-region strand helix
do
	# get per-feature distribution
	fold -w 1 ${OUTPUT_DIR}${feature}_seqs.txt | sort | uniq -c > ${OUTPUT_DIR}${feature}_distr.txt &

done



# let all the distr counters finish
wait



for feature in chain transmembrane-region strand helix
do
	# do with background distribution
	../tsv_to_kmers/generate_random_seqs.py --seqDistr $GLOBAL_DISTR --outputSeqs ${OUTPUT_DIR}${feature}_globalbackground_seqs.txt &
	../tsv_to_kmers/generate_random_seqs.py --seqDistr ${OUTPUT_DIR}${feature}_distr.txt --outputSeqs ${OUTPUT_DIR}${feature}_featurebackground_seqs.txt &

done

