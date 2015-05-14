#!/usr/bin/env python
import argparse
from collections import Counter
from kmer_utils import getKmers, getKmerCounts
import subprocess
import sys
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
  parser.add_argument('--kmerList', help='kmer list file', required=True)
  parser.add_argument('--outputTSV', help='output TSV kmer file', required=True)
  parser.add_argument('--numCts', help='Maximum number of counts to select', required=True, type=int)
  parser.add_argument('--k', help='length of k-mers', required=True, type=int)
  args = parser.parse_args()

  k = int(args.k)
  numCts = int(args.numCts)

  writeAllKmers(k, args.inputTSV, args.kmerList)
  sortedKmerList = getSortedKmerList(args.kmerList, numCts)
  seqsToCounts(k, sortedKmerList, args.inputTSV, args.outputTSV)
  sys.exit(0)

def writeAllKmers(k, input_tsv, kmerList) :
  """
  Write all the kmers present in each sequence to a file
  """

  with open(kmerList, 'w') as out_f :
    for line in open(input_tsv) :
      l = line.strip().split('\t')
      if len(l) < 4 : continue
      for kmer in list(getKmerCounts(l[3], k).elements()) :
        out_f.write(kmer + '\n')


def getSortedKmerList(kmerList, numCts) :
  """
  Sort the kmer list by number of occurances. Return a list of the top numCts kmers in sorted order.
  """

  result = subprocess.check_output(["./get_sorted_kmer_list.sh", kmerList], shell=True)
  return result.strip().split()[:int(numCts)]


def seqsToCounts(k, sortedKmerList, input_tsv, output_path) :
  """
  Reduce each sequence to a set of counts
  """

  with open(output_path, 'w') as out_f :
    out_f.write('#' + '\t'.join(sortedKmerList) + '\n')
    for line in open(input_tsv) :
      l = line.strip().split('\t')
      if len(l) < 4 : continue
      counts = getKmerCounts(l[3], k)
      num_kmers = len(l[3]) - k + 1
      kmers_set = set(counts)
      counts = map(lambda x: str(float(counts[x]) / num_kmers) if x in kmers_set else str(0), sortedKmerList)
      out_f.write('\t'.join(counts) + '\n')

if __name__ == '__main__' : main()

