import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, SimpleDeepRNN


AllModels = ['RNN', 'LSTM']

def simpleLSTM(input_dim) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 256))
    model.add(LSTM(256, 128, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform'))
    model.add(Activation('sigmoid'))
    return model

def simpleRNN(input_dim) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 256))
    model.add(SimpleDeepRNN(256, 128, truncate_gradient=5))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform'))
    model.add(Activation('sigmoid'))
    return model
