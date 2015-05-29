#!/bin/sh

#
# Simple bash script to extract sequences for given labels
#

UNIPROT_TSV=../../uniprot_sprot.xml.tsv
OUTPUT_DIR=../../seq_features/


# schema of uniprot TSV file:
# id	seq_feature.type	seq_feature.description	start	stop	seq

for feature in chain transmembrane-region strand helix
do
	grep $feature $UNIPROT_TSV | awk '{if(length($6) > 9) {print $6}}' > ${OUTPUT_DIR}${feature}_seqs.txt
done

