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
  parser.add_argument('--inputTSV', help='input TSV file, in format of process_tsv.py', required=True)
  parser.add_argument('--outputTSV', help='output TSV kmer file', required=True)
  parser.add_argument('--k', help='length of k-mers', required=True, type=int)
  args = parser.parse_args()

  allKmers(k=int(args.k), input_tsv=args.inputTSV, output_path=args.outputTSV)

def allKmers(k, input_tsv, output_path) :

  """
  Reduce each sequence to a set of counts
  """

  with open(output_path, 'w') as out_f :
    for line in open(input_tsv) :
      l = line.strip().split('\t')
      if len(l) < 4 : continue
      for kmer in list(getKmerCounts(l[3], k).elements()) :
        out_f.write(kmer + '\n')
      

if __name__ == '__main__' : main()
