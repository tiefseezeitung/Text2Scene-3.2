#!/usr/bin/env python3
# -*- coding: utf-8 -*-
    
from hyperopt import hp
from flair.hyperparameter.param_selection import SearchSpace, Parameter
from flair.datasets import ColumnCorpus
from flair.data import Corpus
from flair.embeddings import (
    TokenEmbeddings,
    WordEmbeddings,
    StackedEmbeddings,
    FlairEmbeddings,
    TransformerWordEmbeddings,
    CharacterEmbeddings,)

# this is the folder in which train and test files reside
data_folder = './corpus'

# define columns
columns = {0: 'text', 1: 'iso'}

# load corpus containing training, test and dev data
corpus: Corpus = ColumnCorpus(data_folder, columns,
                                      test_file='test.txt', 
                                      train_file='train.txt')
tag_type = "iso"


# defining our search space
search_space = SearchSpace()

search_space.add(Parameter.EMBEDDINGS, hp.choice, options=[ 
    StackedEmbeddings([WordEmbeddings("glove"),FlairEmbeddings('news-forward'), FlairEmbeddings('news-backward')])
])
# another embedding that could be tried
#WordEmbeddings("glove")
#StackedEmbeddings([FlairEmbeddings('news-forward'), FlairEmbeddings('news-backward')])
#TransformerWordEmbeddings('distilbert-base-uncased', fine_tune=True)
#TransformerWordEmbeddings('distilbert-base-cased', fine_tune=True)

search_space.add(Parameter.HIDDEN_SIZE, hp.choice, options=[64, 128])
search_space.add(Parameter.RNN_LAYERS, hp.choice, options=[1,2])
search_space.add(Parameter.LEARNING_RATE, hp.choice, options=[0.1, 0.15, 0.2])
search_space.add(Parameter.MINI_BATCH_SIZE, hp.choice, options=[8])

#search_space.add(Parameter.DROPOUT, hp.uniform, low=0.0, high=0.5)

from flair.hyperparameter.param_selection import SequenceTaggerParamSelector, OptimizationValue

# create the parameter selector
param_selector = SequenceTaggerParamSelector(
    corpus, 
    'iso', 
    'resources_param_selector/results_flair', 
    max_epochs=15,
    training_runs=2,
    optimization_value=OptimizationValue.DEV_SCORE
)

# start the optimization
param_selector.optimize(search_space, max_evals=20)


