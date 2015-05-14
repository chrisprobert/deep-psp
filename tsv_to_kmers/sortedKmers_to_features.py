#!/usr/bin/env python

import argparse
from collections import Counter
from kmer_utils import getKmers, getKmerCounts


"""
File: sortedKmers_to_features.py

Breakdown a sequence tsv into kmer counts
"""


def main() :
  """
  Read command line arguments and invoke filterTSV()
  """

  parser = argparse.ArgumentParser(description='Filter a uniprot TSV based on annotation')
  parser.add_argument('--inputSeqs', help='input sequence file, one sequence per line', required=True)
  parser.add_argument('--kmerList', help='kmer list file', required=True)
  parser.add_argument('--outputTSV', help='output TSV kmer file', required=True) 
  args = parser.parse_args()

  with open(args.kmerList) as f:
    sortedKmerList = filter(lambda x: len(x.strip()) > 0, f.read().splitlines())

  seqsToCounts(sortedKmerList, args.inputSeqs, args.outputTSV)


def seqsToCounts(sortedKmerList, input_seqs, output_path) :
  """
  Reduce each sequence to a set of counts
  """

  k = len(sortedKmerList[0])

  with open(output_path, 'w') as out_f :
    out_f.write('#' + '\t'.join(sortedKmerList) + '\n')
    for line in open(input_seqs) :
      l = line.strip()
      if len(l) < 1 : continue
      counts = getKmerCounts(l, k)
      num_kmers = len(l) - k + 1
      kmers_set = set(counts)
      counts = map(lambda x: str(float(counts[x]) / num_kmers) if x in kmers_set else str(0), sortedKmerList)
      out_f.write('\t'.join(counts) + '\n')

if __name__ == '__main__' : main()

