#!/usr/bin/env python

import argparse
from collections import Counter
from kmer_utils import getKmers, getKmerCounts
from operator import add

"""
File: get_all_kmers.py

Write a list of all kmers present

"""


def main() :
  """
  Read command line arguments and invoke filterTSV()
  """

  parser = argparse.ArgumentParser(description='Filter a uniprot TSV based on annotation')
  parser.add_argument('--inputSeqs', help='input sequence file, one sequence per line', required=True)
  parser.add_argument('--kmerList', help='output kmer file', required=True)
  parser.add_argument('--k', help='length of k-mers', required=True, type=int)
  args = parser.parse_args()

  allKmers(k=int(args.k), input_seqs=args.inputSeqs, output_path=args.kmerList)

def allKmers(k, input_seqs, output_path) :

  """
  Reduce each sequence to a set of counts
  """

  with open(output_path, 'w') as out_f :
    for line in open(input_seqs) :
      l = line.strip()
      if len(l) < 1 : continue
      for kmer in list(getKmerCounts(l, k).elements()) :
        out_f.write(kmer + '\n')
      

if __name__ == '__main__' : main()
