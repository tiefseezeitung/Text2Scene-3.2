#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sys import exit
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
import csv
import string

def constructtrial(path):
    """Gets data and splits text to tokens and puts them into a list"""
 
    newfile = []
    for subdir, dirs, files in os.walk(path):
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


def construct(attributes, path):
    """constructs a list of lists with entries text, iso, and all given attributes"""
    
    isoents = ['PLACE','PATH','SPATIAL_ENTITY','SPATIAL_SIGNAL',\
              'MOTION','MOTION_SIGNAL','MEASURE','NONMOTION_EVENT']
    newfile = []
    for subdir, dirs, files in os.walk(path):
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
                        for i in isoents:
                            for subelem in elem: 
                                if subelem.tag == i:
                                    if subelem.get('start') == str(token.idx):
                                        txt = subelem.get('text')
                                        # split the token if it consists of 
                                        # more than one word
                                        x = txt.split(" ")
                                        for e in range(len(x)):
                                            newfile += [[x[e],i]+[subelem.get(attributes[a]) for a in range(len(attributes))]]  
                                            # use this instead when you want to put a specific string if an attribute is None:
                                            #newfile += [[x[e],i]+[subelem.get(attributes[a]) if subelem.get(attributes[a])!=None  else '' for a in range(len(attributes))]] 
                                        found = True
                                        break
                    if not found: 
                        #filter out useless data
                        #txt = (str(token.text)).replace('\s','')
                        txt = (str(token.text)).translate(str.maketrans('', '', string.whitespace))
                        if (txt == '' or txt == ' '): 
                            pass
                        else: 
                            newfile += [[txt ,'O']+[None for n in range(len(attributes))]]
                            
    return newfile

def writedata(path,fieldnames,datalist):
    """"writes columns and data in a csv file"""
    
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for each in range(0,len(datalist)):
            writer.writerow({fieldnames[f]: datalist[each][f] for f in range(len(fieldnames))})
            
            
attributes = ['dimensionality','form','motion_type','motion_class',\
              'motion_sense','semantic_type','motion_signal_type']
columnnames = ['text', 'iso'] + attributes

# construct list of lists that will later be converted to csv
trialLst = constructtrial('../Data/spaceeval_trial_data/spaceeval_trial_data') # dev = trial
trainSetClass = construct(attributes,'../Data/training/Traning')
testSetClass = construct(attributes,'../Data/test_task8/Test.configuration3')

print(len(trainSetClass))
print(len(testSetClass))

# write data into csv files
writedata('train_new.csv',columnnames,trainSetClass)
writedata('test_new.csv',columnnames,testSetClass)

# does not produce the desired output for trial, but the trial data is useless anyway
#writedata('trial.csv',['text'],trialLst)


# this part would produce an empyt line after a sentence 
# but it doesn't solve the problems with the corpus 


def prod_lines(file):
    newfile = file.replace('.csv','')+'_wlines.csv'
    with open(file, 'r', encoding='utf-8') as f_input, open(newfile, 'w', encoding='utf-8') as f_output:
        csv_output = csv.writer(f_output, delimiter = ',')
    
        for row in csv.reader(f_input, delimiter = ','):
            if (row[0] == '.' or row[0] == '!' or row[0] == '?'):
                csv_output.writerow(row)
                csv_output.writerow('')
            else:
                csv_output.writerow(row)

prod_lines('train_new.csv')
prod_lines('test_new.csv')