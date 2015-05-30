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
parser.add_argument('--outputName', help='unique output path/name', required=True)
args = parser.parse_args()

assert(args.model in models.AllModels)

print('loading dataset')
# load the input data
X_train, X_test, y_train, y_test = getSplitDataset('transmembrane-region', num_exs=args.numexs,
									bkgrd='global', max_len=100, min_len=10, test_size=0.1)

feature_dim = len(dataset.AAs) + 1

if args.model == 'RNN' :
	model = models.simpleRNN(input_dim=feature_dim)
elif args.model == 'LSTM' :
	model = models.simpleLSTM(input_dim=feature_dim)


print('compiling model')
model.compile(loss='categorical_crossentropy', optimizer='adagrad')

# fit the model
print('fitting model')
fit_results = model.fit(X_train, y_train, nb_epoch=30, batch_size=32,
          validation_split=0.1, shuffle=True, show_accuracy=True, verbose=2)

fit_results = dict(fit_results)
print fit_results
pickle.dump(fit_results, args.outputName + '_fit_results.pkl')

print('saving model')
model.save_weights(args.outputName + '_model_weights')


