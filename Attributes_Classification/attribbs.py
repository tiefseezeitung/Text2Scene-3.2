from flair.data import Sentence
from flair.models import SequenceTagger
import os
from sys import exit
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
from flair.data_fetcher import NLPTaskDataFetcher
from flair.data import Corpus

tagger = SequenceTagger.load('ner')

trialData = '/Users/nihat/Downloads/spaceeval_trial_data'
trainData = '/Users/nihat/Downloads/Traning-2'
testData = '/Users/nihat/Downloads/test_task8-2'
trialCSV = '/Users/nihat/Desktop/trial10.csv'
trainCSV = '/Users/nihat/Desktop/train10.csv'
testCSV = '/Users/nihat/Desktop/test10.csv'


def lstSentences(data):
    """Gets data and splits text to tokens and puts them into a list"""
 
    newfile = []
    for subdir, dirs, files in os.walk('/Users/nihat/Downloads/spaceeval_trial_data'):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".xml"):
                root = ET.parse(filepath)
                t = root.find('TEXT')
                text = t.text
                doc = nlp(text)
                for token in doc:
                    newfile += [token.text]
    return newfile


trialLst = lstSentences(trialData) # dev = trial
print(" ")



def getAttribs(file):
    """predicts attributes"""
    newLst = []
    for subdir, dirs, files in os.walk(file):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".xml"):
                root = ET.parse(filepath)
                t = root.find('TEXT')
                text = t.text
                doc = nlp(text)
                tree = ET.parse(filepath)
                root = tree.getroot()
                doc = nlp(root[0].text)
                for token in doc:
                    found = False

                    for elem in root:
                        for subelem in elem: 
                            #PLACE, NONMOTION_EVENT, SPATIAL_ENTITY, MOTION, MOTION_SIGNAL, SPATIAL_SIGNAL, PATH, MEASURE,     
                            if subelem.tag == "PLACE":
                                if subelem.get('start') == str(token.idx):
                                    newLst += [[subelem.get('text'),'PLACE' ,'dimensionality','form','', '', '', '', '','']]
                                    found = True
                            else: pass
                            
                            if not found:
                                if subelem.tag == "SPATIAL_SIGNAL":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text'),'SPATIAL_SIGNAL' ,'','','', '', '', 'semantic_type', '', '']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "SPATIAL_ENTITY":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text'),'SPATIAL_ENTITY' ,'','form','', '', '', '', '','']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "LOCATION":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text') ,'LOCATION','','','', '', '', '', '','']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "MEASURE":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text'),'MEASURE' ,'','','', '', '', '', '','value']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "MOTION":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text'), 'MOTION', '', '','motion_type','motion_class', 'motion_sense', '','','']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "NONMOTION_EVENT":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text') ,'NONMOTION_EVENT','','','', '', '', '', '','']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "MOTION_SIGNAL":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text'),'MOTION_SIGNAL' ,'','','', '', '', '', 'motion_signal_type','']]
                                        found = True
                            else: pass

                            if not found:
                                if subelem.tag == "PATH":
                                    if subelem.get('start') == str(token.idx):
                                        newLst += [[subelem.get('text'),'PATH' ,'dimensionality','form','', '', '', '', '','']]
                                        found = True
                            else: pass

                    if not found: newLst += [[token.text ,' O','','','', '', '', '', '','']]
        return newLst
                        

 
        
trainSetClass = getAttribs(trainData)
testSetClass = getAttribs(testData)
print("")

import pandas as pd

# erst listen bearbeiten 
# 1.erst keine empty lines
# 2.remove lines with no text
# 3.remove lines with no text but with entity

# 4.add empty lines at the end of a sentence
def updateList(lst):
    # 1.erst keine empty lines
    newLst = []
    for each in range(0,len(lst)):
        # 2und3.erst keine no texts
        if lst[each][0]!= "        " or lst[each][0]!= " " :
            newLst += [lst[each]]
        if lst[each][0]== "." or lst[each][0]== "!" or lst[each][0]== "?":
            newLst += [["",""]]
            
    return newLst
#testSetClass = updateList(testSetClass)
#trainSetClass = updateList(trainSetClass)

import csv

with open(testCSV, 'w', newline='') as csvfile:
    fieldnames = ['text', 'iso','dimensionality','form', 'motion_type', 'motion_class', 'motion_sense', 'semantic_type', 'motion_signal_type', 'value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for each in range(0,len(testSetClass)):
        if testSetClass[each][0] != "        ":
            writer.writerow({'text': testSetClass[each][0], 'iso': testSetClass[each][1]})
        
        
with open(trainCSV, 'w', newline='') as csvfile:
    fieldnames = ['text', 'iso','dimensionality','form', 'motion_type', 'motion_class', 'motion_sense', 'semantic_type', 'motion_signal_type', 'value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for each in range(0,len(trainSetClass)):
        if trainSetClass[each][0] != "        ":
            writer.writerow({'text': trainSetClass[each][0], 'iso': trainSetClass[each][1]})

        
        
with open(trialCSV, 'w', newline='') as csvfile:
    fieldnames = ['text','iso']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for each in range(0,len(trialLst)):
        writer.writerow({'text': trialLst[each]})


print("")


