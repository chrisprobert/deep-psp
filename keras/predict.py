import dataset, models
import numpy as np
from scipy import interp
from sklearn.metrics import roc_curve, auc, f1_score, accuracy_score, precision_score, recall_score
import numpy as np
import sys
import argparse
import pickle


parser = argparse.ArgumentParser(description='Train a model')
parser.add_argument('--model', help='The model to use. Either RNN or LSTM', required=True)
parser.add_argument('--numexs', help='Number of examples', required=True, type=int)
parser.add_argument('--dataname', help='Data file name prefix', required=True)
parser.add_argument('--bkgrd', help='sequence background global/feature', required=False, default='global')
parser.add_argument('--task', help='task name', required=False, default='transmembrane-region')
args = parser.parse_args()

input_dim = len(dataset.AAs) + 1

#
# Model Specific Settings - need to change these based on the model
#
NUMEXS = args.numexs
DATA_NAME = args.dataname
model = models.getModel(args.model, input_dim)
background = args.bkgrd

# load training/test data
X_train, X_test, y_train, y_test = dataset.getSplitDataset(
    args.task, num_exs=NUMEXS, bkgrd=background, 
    max_len=100, min_len=10, test_size=0.1)

model.compile(loss='categorical_crossentropy', optimizer='adagrad')

weights_path = '/home/gene245/cprobert/deep-psp/keras/output/' + DATA_NAME + '_model_weights.hdf5'
model.load_weights(weights_path)

test_preds = model.predict(X_test)
train_preds = model.predict(X_train)

# save our results in a dictionary
classif_results = {
    'test_preds' : test_preds,
    'train_preds' : train_preds,
    'y_train' : y_train,
    'y_test' : y_test
}

pkl_path = '/home/gene245/cprobert/deep-psp/keras/output/' + DATA_NAME + '_train_test_preds.pkl'

pickle.dump(classif_results, open(pkl_path, 'w'))


