from rest_framework.views import APIView
from rest_framework.response import Response

import os
import torch
# from torchtext import data
import dill
import torch.nn as nn
import spacy

nlp = spacy.load('en')

txt_field = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(_file_))), "ml", "TEXT.Field")
        
with open(txt_field,"rb")as f:
    TEXT=dill.load(f)

# to clean data
def normalise_text (text):
    text = text.lower() # lowercase
    text = text.replace(r"\#","") # replaces hashtags
    text = text.replace(r"http\S+","URL")  # remove URL addresses
    text = text.replace(r"@","")
    text = text.replace(r"[^A-Za-z0-9()!?\'\`\"]", " ")
    text = text.replace("\s{2,}", " ")
    return text

def predict(model, sentence):
    sent=normalise_text(sentence)
    # print(sent)
    tokenized = [tok.text for tok in nlp.tokenizer(sent)]  #tokenize the sentence 
    indexed = [TEXT.vocab.stoi[t] for t in tokenized]          #convert to integer sequence
    length = [len(indexed)]                                    #compute no. of words
    tensor = torch.LongTensor(indexed)            #convert to tensor
    tensor = tensor.unsqueeze(1).T                             #reshape in form of batch,no. of words
    length_tensor = torch.LongTensor(length)                   #convert to tensor
    prediction = model(tensor, length_tensor)                  #prediction 
    return prediction.item() 

class classifier(nn.Module):
    
    #define all the layers used in model
    def _init_(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, 
                 bidirectional, dropout):
        
        #Constructor
        super()._init_()          
        
        #embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        #lstm layer
        self.rnn = nn.RNN(embedding_dim, 
                           hidden_dim, 
                           num_layers=n_layers, 
                           bidirectional=bidirectional, 
                           dropout=dropout,
                           batch_first=True)
        
        #dense layer
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        
        #activation function
        self.act = nn.Sigmoid()
        
    def forward(self, text, text_lengths):
        
        #text = [batch size,sent_length]
        embedded = self.embedding(text)
        #embedded = [batch size, sent_len, emb dim]
      
        #packed sequence
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths,batch_first=True)
        
        packed_output, hidden = self.rnn(packed_embedded)
        #hidden = [batch size, num layers * num directions,hid dim]
        #cell = [batch size, num layers * num directions,hid dim]
        
        #concat the final forward and backward hidden state
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim = 1)
                
        #hidden = [batch size, hid dim * num directions]
        dense_outputs=self.fc(hidden)

        #Final activation function
        outputs=self.act(dense_outputs)
        
        return outputs

class FakeNewsCheckerView(APIView):
    
    def get(self, request, *args, **kwargs):
        SEED = 1234
        torch.manual_seed(SEED)
        torch.backends.cudnn.deterministic = True
        
        #define hyperparameters
        size_of_vocab = 7965
        embedding_dim = 100
        num_hidden_nodes = 32
        num_output_nodes = 1
        num_layers = 2
        bidirection = True
        dropout = 0.2

        path_wts = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(_file_))), "ml", "saved_weights.pt")
        model1 = classifier(size_of_vocab, embedding_dim, num_hidden_nodes,num_output_nodes, num_layers, 
                   bidirectional = True, dropout = dropout)
        model1.load_state_dict(torch.load(path_wts))
        model1.eval()
       

        news = request.query_params.get('news')
        title = request.query_params.get('title')
        author = request.query_params.get('author')
        total = str(title)+str(author)+str(news)
        val = predict(model1, total)
        print(val)
        if val>=0.5:
            res=1
        else:
            res=0
        return Response({"isTrue": res})
