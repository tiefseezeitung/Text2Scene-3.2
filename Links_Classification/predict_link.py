#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flair.models import SequenceTagger
from flair.data import Sentence

def predict(sentence, link):
    '''tags sentence with link predictor and returns sentence'''
    if link == 'olink':
        olink_tagger = SequenceTagger.load('resources/taggers/olink/final-model.pt')
        olink_tagger.predict(sentence)
    elif link == 'qslink':
        qslink_tagger = SequenceTagger.load('resources/taggers/qslink/final-model.pt')
        qslink_tagger.predict(sentence)
    return sentence

# create example sentence 
sentence = Sentence('I live in Berlin.')


link = 'qslink' #CHOOSE 'qslink' OR 'olink'
sentence = predict(sentence, link)

print()
print(sentence.to_tagged_string())