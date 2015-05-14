#!/usr/bin/env python

import argparse

"""
File: generate_random_seqs.py

Generate random sequences with the same AA distribution as the original set of sequences,
and the same number of sequences as the original set.


"""


def main() :
  """
  Read command line arguments and invoke filterTSV()
  """

  parser = argparse.ArgumentParser(description='Filter a uniprot TSV based on annotation')
  parser.add_argument('--inputSeqs', help='Input sequence file. Should only contain sequences.', required=True)
  parser.add_argument('--outputSeqs', help='output sequence file', required=True)
  args = parser.parse_args()

  allKmers(k=int(args.k), input_tsv=args.inputTSV, output_path=args.kmerList)

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

def getSeqDistr(infile) :
  ret = {}
  for line in open(infile) :
    for c in line.strip() :
      if c not in ret :
        ret[c] = 1
      else ret[c] += 1
  tot_chars = sum(ret.values())
  for k in ret :
    ret[k] = float(ret[k]) / tot_chars
  return ret


if __name__ == '__main__' : main()
