import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, SimpleDeepRNN


def simpleLSTM(input_dim) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 256))
    model.add(LSTM(256, 128, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform', activation='sigmoid'))
    return model

def LSTM512(input_dim) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 512))
    model.add(Dropout(0.25))
    model.add(LSTM(512, 256, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(256, 128, init='uniform', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform', activation='softmax'))
    return model

def simpleRNN(input_dim) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 256))
    model.add(SimpleDeepRNN(256, 128, truncate_gradient=5))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform'))
    model.add(Activation('sigmoid'))
    return model

def RNN512(input_dim) :
    model = keras.models.Sequential()
    model.add(Embedding(input_dim, 512))
    model.add(Dropout(0.5))
    model.add(SimpleDeepRNN(512, 256, depth=10, truncate_gradient=10))
    model.add(Dropout(0.5))
    model.add(Dense(256, 128, init='uniform', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform', activation='softmax'))
    return model

def GRU512(input_dim) :
	model = keras.models.Sequential()
    model.add(Embedding(input_dim, 512))
    model.add(Dropout(0.5))
	keras.layers.recurrent.GRU(512, 256, truncate_gradient=10)
	model.add(Dropout(0.5))
	model.add(Dense(256, 128, init='uniform', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, 2, init='uniform', activation='softmax'))
    return model

Models = {'RNN':simpleRNN, 'LSTM':simpleLSTM, 'LSTM512':LSTM512, 'RNN512':RNN512, 'GRU512':GRU512}
AllModels = Models.keys()

def getModel(model_name, input_dim) :
	return Models[model_name](input_dim)

