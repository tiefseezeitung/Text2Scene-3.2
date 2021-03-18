#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# programme not running, still dimension error

# this model is not trained through flair, we extract input from flair corpus 
# and use their embeddings

from flair.embeddings import (
    TokenEmbeddings,
    WordEmbeddings,
    StackedEmbeddings,
    FlairEmbeddings,
    TransformerWordEmbeddings)
from flair.data import Corpus
from flair.datasets import ColumnCorpus
#from matplotlib import pyplot as plt
import torch
import torch.nn as nn
from torch.autograd import Variable
from sys import exit

data_folder = './model 1'
columns = {0: 'text', 1:'iso', 2:'dimensionality', 3:'form', 4:'motion_type',\
           5:'motion_class', 6:'motion_sense', 7:'semantic_type', \
               8:'motion_signal_type'}

corpus: Corpus = ColumnCorpus(data_folder, columns,
                          train_file='train.txt', 
                          test_file='test.txt', column_delimiter='\t', )

tag_type = 'dimensionality'

tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
#print(tag_dictionary)

embedding_types = [
    
        WordEmbeddings('glove', ),
    
        # comment in this line to use character embeddings
        #CharacterEmbeddings(),
    
        # comment in these lines to use flair embeddings
        #FlairEmbeddings('news-forward-fast'),
        #FlairEmbeddings('news-backward-fast'),
    ]
 
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

def get_vec(iso_tag, prob, embedding): 
    # adds a vector to our word_embedding (this increases the length of our embedding)

    isoents = ['SPATIAL_ENTITY', 'PATH', 'PLACE', 'MEASURE', 'MOTION', \
               'NONMOTION_EVENT', 'MOTION_SIGNAL', 'SPATIAL_SIGNAL', 'O']
    vec = torch.zeros(len(isoents))
    vec[isoents.index(iso_tag)] = prob
    
    vec = torch.cat((embedding, vec))
    
    return vec


def get_categ_tensor(category, lst):
    # return tensor of given class / tag
    vec = torch.zeros(len(lst))
    vec[lst.index(category)] = 1
    return vec

train = corpus.train + corpus.dev
test = corpus.test #not used yet, needed later for testing

train_tensors = [] #list of input vectors
tags = [] #list of all tags
length_train = 0

for sentence in train:
    embeddings.embed(sentence)
    length_train += len(sentence)
    
    for token in sentence:
        #print(token.embedding.size())
        #print(token,token.text,token.idx,token.get_tag('iso'))
        iso = str(token.get_tag('iso')).split(' (')[0]
        prob = float((str(token.get_tag('iso')).split('(')[1]).split(')')[0])
        
        vector=get_vec(iso, prob, token.embedding)
        train_tensors.append(vector)
        
        tag = str(token.get_tag(tag_type)).split(' (')[0]
        tags.append(tag)
        

output_classes = list(set(tags))
print(output_classes)
print(len(output_classes))

# try a RNN
class RNN(nn.Module):
    '''Class for a classifying RNN'''
    def __init__(self,input_size,hidden_size,output_size):
        super(RNN,self).__init__()
        
        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.logsoftmax = nn.LogSoftmax(dim=1)
        
    def forward(self, input_tensor, hidden_tensor):
        combined = torch.cat((input_tensor, hidden_tensor))
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        return output, hidden

    def init_hidden(self):
        return (torch.zeros(self.hidden_size))
    
    def train(self, input_tensor, category_tensor): #train method for RNN class
        criterion = nn.CrossEntropyLoss()
        lr = 0.1
        optimizer = torch.optim.SGD(net.parameters(),lr=lr)    
        
        hidden = self.init_hidden()
        
        output, hidden = self(input_tensor, hidden)
            
        optimizer.zero_grad()
        loss = criterion(output, category_tensor)
        loss.backward()
        optimizer.step()
            
        return output,loss.item()
    
# try a normal NN 
class NN(nn.Module):
    '''classification NN is created with two hidden layers'''
    def __init__(self,input_size, hidden_size, output_size):
        super(NN,self).__init__()
        
        self.hid1 = nn.Linear(input_size, hidden_size)
        self.hid2 = nn.Linear(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        
        torch.nn.init.xavier_uniform_(self.hid1.weight)
        torch.nn.init.zeros_(self.hid1.bias)
        torch.nn.init.xavier_uniform_(self.hid2.weight)
        torch.nn.init.zeros_(self.hid2.bias)
        torch.nn.init.xavier_uniform_(self.out.weight)
        torch.nn.init.zeros_(self.out.bias)
        
    def forward(self, input_tensor):
        z = torch.tanh(self.hid1(input_tensor))
        z = torch.tanh(self.hid2(z))
        z = self.out(z) 
        return z
    
    def train(self, input_tensor, category_tensor): #train method for NN class
        criterion = nn.CrossEntropyLoss()
        lr = 0.1
        optimizer = torch.optim.SGD(net.parameters(),lr=lr)

        output = self(input_tensor)
            
        optimizer.zero_grad()
        loss = criterion(output, category_tensor)
        loss.backward()
        optimizer.step()
            
        return output,loss.item()
        
# define your neural net
#net = RNN(len(train_tensors[0]),128,len(output_classes))  #first try
net = NN(len(train_tensors[0]),128,len(output_classes))  #second try with NN


avg = [] #average losses are saved into this list
sum = 0
#this is 1 epoch:
for i in range(length_train):
    output, loss = net.train(Variable(train_tensors[i]), Variable(get_categ_tensor(tags[i], output_classes)))
    sum = sum + loss
    if i % 100 == 0:
        avg.append(sum/100)
        sum = 0
        print(100*i/length_train,'% progress')
        
#plt.figure()
#plt.plot(avg)
#plt.show()