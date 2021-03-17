#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flair.models import SequenceTagger, MultiTagger
from flair.data import Corpus, Sentence

def predict(sentence, iso=False):
    '''Predicts the attribute tags of the tokens in the given sentence. There are
    two different models, you can choose by setting the iso variable'''
    
    attributes = ['dimensionality', 'form', 'motion_type', 'motion_class', 'motion_sense',\
                  'semantic_type', 'motion_signal_type']
        
    if not iso:
        #if you want to use the attribute tagger without the iso information

        tagger = MultiTagger.load(['model 1/resources/taggers/'+a+'/final-model.pt' for \
                                   a in attributes])
                         
        tagger.predict(sentence)
    else:
        # this is the tagger with the iso information (given in sentence as tokens), 
        # without the iso tagger model does not work
        isotagger = SequenceTagger.load('../Iso_Entities_Classification/resources/taggers/iso_flair/final-model.pt')

        tagger = MultiTagger.load(['model 2/resources_ilines/taggers/'+a+'/final-model.pt' for \
                                   a in attributes])
            
        isotagger.predict(sentence)
        sentence = Sentence(str(sentence.to_tagged_string()))
        tagger.predict(sentence)
        
                
    return sentence
        

# create example sentence 
sentence = Sentence('I live in Berlin.')
# use predict function 
sentence = predict(sentence)

print()
print(sentence.to_tagged_string())
