#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flair.models import SequenceTagger, MultiTagger
from flair.data import Corpus, Sentence

def predict(sentence, iso=True):
    attributes = ['dimensionality', 'form', 'motion_type', 'motion_class', 'motion_sense',\
                  'semantic_type', 'motion_signal_type']
        
    if not iso:
        #if you want to use the attribute tagger without the iso information
        tagger = MultiTagger.load(['resources/taggers/dimensionality/final-model.pt',\
                                   'resources/taggers/form/final-model.pt',\
                                   'resources/taggers/motion_type/final-model.pt',
                                   'resources/taggers/motion_class/final-model.pt',
                                   'resources/taggers/motion_sense/final-model.pt',
                                   'resources/taggers/semantic_type/final-model.pt',
                                   'resources/taggers/motion_signal_type/final-model.pt',
                                   ])
        tagger.predict(sentence)
    else:
        #this is the tagger with the iso information
        isotagger = SequenceTagger.load('resources/taggers/iso/final-model.pt')
        tagger = MultiTagger.load(['resources_ilines/taggers/dimensionality/final-model.pt',\
                                   'resources_ilines/taggers/form/final-model.pt',\
                                   'resources_ilines/taggers/motion_type/final-model.pt',
                                   'resources_ilines/taggers/motion_class/final-model.pt',
                                   'resources_ilines/taggers/motion_sense/final-model.pt',
                                   'resources_ilines/taggers/semantic_type/final-model.pt',
                                   'resources_ilines/taggers/motion_signal_type/final-model.pt',
                                   ])
        isotagger.predict(sentence)
        sentence = Sentence(str(sentence.to_tagged_string()))
        tagger.predict(sentence)
    return sentence
        

# create example sentence 
sentence = Sentence('I live in Berlin.')
# use predict function 
sentence = predict(sentence)
print(sentence)