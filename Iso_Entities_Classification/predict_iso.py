#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flair.models import SequenceTagger
from flair.data import Sentence

model = SequenceTagger.load('resources/taggers/iso_glove/final-model.pt')

# create example sentence
sentence = Sentence('I live in Berlin.')

# predict tags and print
model.predict(sentence)

print(sentence.to_tagged_string())
print()
for entity in sentence.get_spans('iso'):
    print(entity)
