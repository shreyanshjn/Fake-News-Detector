from rest_framework.views import APIView
from rest_framework.response import Response

import os
from keras.preprocessing.text import Tokenizer
import pandas as pd
import pickle

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding, SimpleRNN
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from tensorflow import keras  
from keras.preprocessing import sequence
from keras.callbacks import EarlyStopping

class FakeNewsCheckerView(APIView):
    
    def get(self, request, *args, **kwargs):
        news = request.query_params.get('news')
        title = request.query_params.get('title')
        author = request.query_params.get('author')
        total = str(title)+' '+str(author)+' '+str(news)

        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "model1.h5")
        tokenizer_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "tokenizer.pickle")
        
        
        with open(tokenizer_path, 'rb') as handle:
            tok = pickle.load(handle)
        
        model = keras.models.load_model(model_path)
        
        seq = tok.texts_to_sequences([total])
        ts = sequence.pad_sequences(seq,maxlen=350)

        val = model.predict(ts)[0][0]
        print(val)
        if val>=0.5:
            res=1
        else:
            res=0
        return Response({"isTrue": res})
    