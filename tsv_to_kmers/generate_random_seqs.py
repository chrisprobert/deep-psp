#!/usr/bin/env python

import argparse
import numpy as np

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
  parser.add_argument('--seqDistr', help='Input sequence distribution. Should have <count> <letter> format.', required=True)
  parser.add_argument('--outputSeqs', help='Output sequence file.', required=True)
  parser.add_argument('--inputSeqs', help='Input sequence file. Only used to get length, not sequence content.', required=True)
  args = parser.parse_args()

  distr = getSeqDistr(args.seqDistr)
  getRandomSeqs(distr, args.inputSeqs, args.outputSeqs)

def getRandomSeqs(distr, infile, outfile) :
  chars = distr.keys()
  probs = distr.values()

  with open(infile) as f_in :
    with open(outfile, 'w') as f_out :
      for line in f_in :
        for i in range(len(line.strip())) :
          indx = np.argmax(np.random.multinomial(1, probs))
          f_out.write(chars[indx])
        f_out.write('\n')


def getSeqDistr(infile) :
  dist = {}
  for line in open(infile) :
    l = line.strip().split()
    if len(l) != 2 : continue
    dist[l[1]] = float(l[0])
  tot_chars = sum(dist.values())
  for k in dist :
    dist[k] = dist[k] / tot_chars
  return dist


if __name__ == '__main__' : main()
