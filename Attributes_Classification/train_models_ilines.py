#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import DocumentLSTMEmbeddings
from flair.embeddings import (
    TokenEmbeddings,
    WordEmbeddings,
    StackedEmbeddings,
    FlairEmbeddings,
    TransformerWordEmbeddings,
    CharacterEmbeddings,)
from flair.models import SequenceTagger, MultiTagger
from flair.datasets import ColumnCorpus
from flair.trainers import ModelTrainer
from flair.datasets import CSVClassificationCorpus
from flair.data import Corpus
from pathlib import Path
from typing import List
from sys import exit

def train(attributes, index):
    
    data_folder = './'
    columns = {0: 'text', index+1:attributes[index]}
    
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train_ilines.txt',
                              test_file='test_ilines.txt')
    
    tag_type = attributes[index]
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    
    print(corpus)
    print(corpus.obtain_statistics())
    embedding_types = [
        
            WordEmbeddings('glove'),
        
            # comment in this line to use character embeddings
            #CharacterEmbeddings(),
        
            # comment in these lines to use flair embeddings
            FlairEmbeddings('news-forward-fast'),
            FlairEmbeddings('news-backward-fast'),
        ]
 
    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
    
    tagger: SequenceTagger = SequenceTagger(hidden_size=128,
                                                embeddings=embeddings,
                                                tag_dictionary=tag_dictionary,
                                                tag_type=tag_type,
                                                use_crf=True)
    trainer = ModelTrainer(tagger, corpus)
    trainer.train("resources_ilines/taggers/"+attributes[index], 
                  learning_rate=0.1, 
                  max_epochs=8)  # if performace is bad set mini_batch_size=8

attributes = ['dimensionality', 'form', 'motion_type', 'motion_class', 'motion_sense',\
              'semantic_type', 'motion_signal_type']

# we want to train all attributes individually thus we want:
for i in range(len(attributes)):
    train(attributes, i)

# to not overload your computer we rather train them carefully and edit index
# after each time
#train(attributes, 0)

