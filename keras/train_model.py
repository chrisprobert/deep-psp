import keras
from keras.optimizers import SGD

import models
import dataset

import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
import pickle


parser = argparse.ArgumentParser(description='Train a model')
parser.add_argument('--model', help='The model to use. Either RNN or LSTM', required=True)
parser.add_argument('--numexs', help='Number of examples', required=True, type=int)
parser.add_argument('--numepochs', help='Number of epochs', required=True, type=int)
parser.add_argument('--outputName', help='unique output path/name', required=True)
parser.add_argument('--bkgrd', help='sequence background global/feature', required=False, default='global')
args = parser.parse_args()

assert(args.model in models.AllModels)
assert(args.bkgrd in ['global', 'feature'])

print 'using parameters:\n', vars(args)

print '--loading dataset--'
# load the input data
X_train, X_test, y_train, y_test = dataset.getSplitDataset('transmembrane-region', num_exs=args.numexs,
									bkgrd=args.bkgrd, max_len=100, min_len=10, test_size=0.1)

feature_dim = len(dataset.AAs) + 1

model = models.getModel(args.model, feature_dim)

print '--compiling model--'
model.compile(loss='categorical_crossentropy', optimizer='adagrad')

# fit the model
print '--fitting model--'
fit_results = model.fit(X_train, y_train, nb_epoch=args.numepochs, batch_size=32,
          validation_split=0.1, shuffle=True, show_accuracy=True, verbose=2)

print fit_results
pickle.dump(fit_results, open(args.outputName + '_fit_results.pkl', 'w'))

print '--saving model--'
model.save_weights(args.outputName + '_model_weights.hdf5')


