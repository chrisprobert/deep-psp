import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, SimpleDeepRNN
import keras.preprocessing.sequence
from keras.optimizers import SGD

from sklearn.cross_validation import train_test_split

import matplotlib.pyplot as plt
import numpy as np
import pandas as ps
import sys
import argparse

import dataset

R_SEED=42

parser = argparse.ArgumentParser(description='Train a model')
parser.add_argument('--model', help='The model to use. Either RNN or LSTM', required=True)
parser.add_argument('--numexs', help='Number of examples', required=True, type=int)
args = parser.parse_args()

assert(args.model in ['RNN', 'LSTM'])

def getsimpleLSTM(input_dim=len(dataset.AAs)+1) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 256))
    model.add(Dropout(0.5))
    model.add(LSTM(256, 128, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.2))
    model.add(Dense(128, 1, init='uniform'))
    model.add(Activation('sigmoid'))
    return model

def getsimpleRNN(input_dim=len(dataset.AAs)+1) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 256))
    model.add(Dropout(0.5))
    model.add(SimpleDeepRNN(256, 128, truncate_gradient=5))
    model.add(Dropout(0.2))
    model.add(Dense(128, 1, init='uniform'))
    model.add(Activation('softmax'))
    return model

# Load the input data, and split the test data
seqs, labels = dataset.loadShuffledData('transmembrane-region', num_exs=int(args.numexs), bkgrd='global', max_len=100, min_len=10)
X_train, X_test, y_train, y_test = train_test_split(seqs, labels, test_size=0.1, random_state=R_SEED)

# Declare and compile the model
if args.model == 'RNN' :
	print('using RNN model')
	model = getsimpleRNN()
else :
	print('using LSTM model')
	model = getsimpleLSTM()

print('compiling model')
model.compile(loss='binary_crossentropy', optimizer='adagrad')

# fit the model
print('fitting model')
model.fit(X_train, y_train, nb_epoch=30, batch_size=16,
          validation_split=0.1, shuffle=True, show_accuracy=True)

score = model.evaluate(X_test, y_test, batch_size=16)
print score















