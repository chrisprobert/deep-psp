"""

File: kmer_utils.py

Utilities to help with converting sequences into kmer counts.

"""

def getKmers(seq, k) :
  """
  Return a list of k-mers for the sequence region
  """
  return map(lambda x: seq[x:x+k], range(len(seq) - k + 1))

