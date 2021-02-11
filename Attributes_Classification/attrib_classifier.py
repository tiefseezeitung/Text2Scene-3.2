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
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.datasets import CSVClassificationCorpus
from flair.data import Corpus
from pathlib import Path
from typing import List
from sys import exit



label_columns = ['iso', 'dimensionality', 'form', 'motion_type', 'motion_class', 'motion_sense',\
             'semantic_type', 'motion_signal_type']
column_name_map = {0: 'text', 1: 'label-iso',2:'label-dimensionality', 3:'label-form',4:'label-motion_type',5:'label-motion_class',6:'label-motion_sense',\
              7:'label-semantic_type',8:'label-motion_signal_type'}

data_folder = './'

# 3 different functions for corpus

#1 labels get recognized, sentences do not
#we get messages:'Warning: An empty Sentence was created! Are there empty strings in your dataset?'
#resulting error: RuntimeError: Length of all samples has to be greater than 0, but found an element in 'lengths' that is <= 0

corpus: Corpus = CSVClassificationCorpus(data_folder, column_name_map, skip_header=True, test_file='test.csv',train_file='train.csv',delimiter=',')


#2 sentences get recognized, but labels do not

#corpus = NLPTaskDataFetcher.load_column_corpus(Path('./'), column_name_map, train_file='train.csv', test='test_orig.csv')


#3 does not recognize anything in this format

#corpus = NLPTaskDataFetcher.load_classification_corpus(Path('./'), train_file='train.csv',test_file='test.csv')

print(corpus)
print(corpus.obtain_statistics())

exit()

word_embeddings = [WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')]
document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)


classifier = TextClassifier(document_embeddings, \
                label_dictionary=corpus.make_label_dictionary(), multi_label=True)
    

trainer = ModelTrainer(classifier, corpus)
trainer.train("resources/taggers/example-attr", max_epochs=10)
