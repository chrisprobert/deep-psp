#!/usr/bin/env python

import argparse
from collections import Counter
from kmer_utils import getKmers, getKmerCounts
from operator import add

"""
File: tsv_to_kmers.py

Breakdown a sequence tsv into kmer counts
"""


def main() :
  """
  Read command line arguments and invoke filterTSV()
  """

  parser = argparse.ArgumentParser(description='Filter a uniprot TSV based on annotation')
  parser.add_argument('--inputTSV', help='input TSV file, in format of process_tsv.py', required=True)
  parser.add_argument('--outputTSV', help='output TSV kmer file', required=True)
  parser.add_argument('--numCts', help='Maximum number of counts to select', required=True, type=int)
  parser.add_argument('--k', help='length of k-mers', required=True, type=int)
  args = parser.parse_args()

  seqsToCounts(k=int(args.k), numCts=int(args.numCts), input_tsv=args.inputTSV, output_path=args.outputTSV)

def seqsToCounts(k, numCts, input_tsv, output_path) :

  """
  Reduce each sequence to a set of counts
  """

  # first pass through to get the total set of counts
  total_counts = []
  for line in open(input_tsv) :
    l = line.strip().split('\t')
    if len(l) < 4 : continue
    total_counts.append(getKmerCounts(l[3], k))

  top_counts_list = list(reduce(add, total_counts).most_common(numCts))

  with open(output_path, 'w') as out_f :
    out.write('#' + '\t'.join(top_counts_list) + '\n')

    for line in open(input_tsv) :
      l = line.strip().split('\t')
      if len(l) < 4 : continue
      counts = getKmerCounts(l[3], k)
      num_kmers = sum(counts.values())
      kmers = set(counts)
      counts = map(lambda x: str(float(counts[x]) / num_kmers) if x in kmers else str(0), top_counts_list)
      out_f.write('\t'.join(counts) + '\n')

if __name__ == '__main__' : main()
