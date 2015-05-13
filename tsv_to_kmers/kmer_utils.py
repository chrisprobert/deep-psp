"""

File: kmer_utils.py

Utilities to help with converting sequences into kmer counts.

"""

from collections import Counter


def getKmers(seq, k) :
  """
  Return a list of k-mers for the sequence region
  """
  return map(lambda x: seq[x:x+k], range(len(seq) - k + 1))

def getKmerCounts(seq, k) :
  """
  Return a Counter of kmer -> counts for this sequence
  """
  return Counter(getKmers(seq, k))