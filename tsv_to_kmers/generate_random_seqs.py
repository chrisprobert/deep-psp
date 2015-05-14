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
  parser.add_argument('--inputSeqs', help='Input sequence file. Should only contain sequences. One sequence per line.', required=True)
  parser.add_argument('--outputSeqs', help='Output sequence file.', required=True)
  args = parser.parse_args()

  distr = getSeqDistr(args.inputSeqs)
  getRandomSeqs(distr, args.inputSeqs, args.outputSeqs)

def getRandomSeqs(distr, infile, outfile) :
  chars = distr.keys()
  probs = distr.values()

  with open(infile) as f_in :
    with open(outfile, 'w') as f_out :
      for line in f_in :
        for i in len(line.strip()) :
          indx = np.argmax(np.random.multinomial(1, probs))
          f_out.write(chars[indx])
        f_out.write('\n')


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
