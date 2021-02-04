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

'''programme does not work, multiple messages like: 
    Warning: An empty Sentence was created! Are there empty strings in your dataset?
resulting error: RuntimeError: Length of all samples has to be greater than 0, but found an element in 'lengths' that is <= 0'''


column_name_map = {0: 'text', 1: 'label', 2:'label',3:'label',4:'label',5:'label',\
              6:'label',7:'label',8:'label'}
data_folder = './'

corpus: Corpus = CSVClassificationCorpus(data_folder, column_name_map, skip_header=True, test_file='test.csv',train_file='train.csv',delimiter=',')
print(corpus)

word_embeddings = [WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'), FlairEmbeddings('news-backward-fast')]
document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)

'''
embedding_types: List[TokenEmbeddings] = [
    WordEmbeddings("glove"),
    #TransformerWordEmbeddings('distilbert-base-uncased', fine_tune=True),
    # comment in this line to use character embeddings
    # CharacterEmbeddings(),
    # comment in these lines to use contextual string embeddings
    #
    # FlairEmbeddings('news-forward'),
    #
    # FlairEmbeddings('news-backward'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
'''


classifier = TextClassifier(document_embeddings, \
                label_dictionary=corpus.make_label_dictionary(), multi_label=True)
    

trainer = ModelTrainer(classifier, corpus)
trainer.train("resources/taggers/example-attr", max_epochs=10)
