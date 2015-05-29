import numpy as np
import sys
from sklearn.cross_validation import train_test_split

R_SEED=42

#
# The character mapping to encode amino acid sequences.
# Non-AA chars should be mapped to X, or 0.
#

AAs = ['X','I','L','V','F','M','C','A','G','P','T','S','Y','W','Q','N','H','E','D','K','R']
AAIndexes = {AAs[i] : i for i in range(len(AAs))}

def encodeAA(x) :
    # Encode an amino acid sequence
    if x not in AAIndexes :
        return 0
    return AAIndexes[x]

def seqToIdxs(seq) :
    return map(encodeAA, seq.strip().upper())

#
#  Functions for loading sequences and background distributions
#

def loadSeqs(seqs_file, num_lines=sys.maxint, min_len=0) :
    seqs = []
    with open(seqs_file) as in_f :
        for line in in_f :
            if len(line.strip()) >= min_len :
                seqs.append(seqToIdxs(line))
            if len(seqs) >= num_lines : break
    return seqs

def loadFeatureSeqs(task_name, num_lines=sys.maxint, min_len=0) :
    path = '/home/gene245/cprobert/seq_features/%s_seqs.txt' % task_name
    return loadSeqs(path, num_lines, min_len)

def loadFeatureBkgrdSeqs(task_name, num_lines=sys.maxint, min_len=0) :
    path = '/home/gene245/cprobert/seq_features/%s_featurebackground_seqs.txt' % task_name
    return loadSeqs(path, num_lines, min_len)

def loadGlobalBkgrdSeqs(task_name, num_lines=sys.maxint, min_len=0) :
    path = '/home/gene245/cprobert/seq_features/%s_globalbackground_seqs.txt' % task_name
    return loadSeqs(path, num_lines, min_len)

def createBinaryLabelVector(length, label) :
    if label == 1 :
        return np.ones(length, dtype=int)
    return np.zeros(length, dtype=int)

def createOneHotLabels(length, label) :
    ar = [1,0] if label == 0 else [0,1]
    ar = [ar for i in xrange(length)]
    return np.array(ar)

def loadShuffledData(task_name, num_exs=sys.maxint, bkgrd='global', max_len=100, min_len=10) :
    """
    Loads a shuffled set of (seqs, labels) for the given task.
    """
    assert(bkgrd in ['global', 'feature'])
    seqs_pos = loadFeatureSeqs(task_name,num_exs/2)
    if bkgrd == 'global' :
        seqs_neg = loadGlobalBkgrdSeqs(task_name,num_exs/2)
    else :
        seqs_neg = loadFeatureBkgrdSeqs(task_name,num_exs/2)
    seqs = keras.preprocessing.sequence.pad_sequences(seqs_pos + seqs_neg, maxlen=max_len)
    labels = np.append(createOneHotLabels(len(seqs_pos), 1),
                       createOneHotLabels(len(seqs_neg), 0), axis=0)
    np.random.seed(R_SEED)
    idxs = np.arange(labels.shape[0])
    np.random.shuffle(idxs)
    seqs, labels = seqs[idxs], labels[idxs]
    return seqs, labels

def getSplitDataset(task_name, num_exs=sys.maxint, bkgrd='global', max_len=100, min_len=10, test_size=0.1) :
    seqs, labels = loadShuffledData(task_name, num_exs, bkgrd, max_len, min_len)
    return train_test_split(seqs, labels, test_size=test_size, random_state=R_SEED)
