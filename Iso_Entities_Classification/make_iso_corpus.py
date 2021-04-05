#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
import string



def construct(path):
    """constructs a list of [token, iso entity] entries and returns this list"""
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
                isoents = ['PLACE','PATH','SPATIAL_ENTITY','SPATIAL_SIGNAL',\
                           'MOTION','MOTION_SIGNAL','MEASURE','NONMOTION_EVENT']
                prev = 1
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
                                        x = txt.split(' ')
                                        for e in range(0,len(x)):
                                                if (str(x[e])).translate(str.maketrans('', '', string.whitespace)) =='':
                                                    pass #filter out useless data
                                                else:
                                                    newfile += [[x[e], i]]
                                        found = True
                                        prev = len(x)
                                        break
                    if not found: 
                        if prev > 1: prev -= 1
                        else:
                            x = token.text.split(' ')
                            for e in range(len(x)):
                                if (str(x[e])).translate(str.maketrans('', '', string.whitespace)) == '': 
                                    pass #filter out useless data
                                else: 
                                    newfile += [[x[e], 'O']]
    return newfile

def write_txt(path,fieldnames,datalist):
    """"Writes data rowwise into a string, separation between entries with 
    tab \t. Then writes this string into a txtfile with passed name/path 'path'"""
    
    string = ''
    for each in range(0,len(datalist)):
        # one row
        for e in range(len(datalist[each])):
            # column
            if datalist[each][e] != None:
                string+= str(datalist[each][e])
                if e == len(datalist[each])-1: string += '\n'
                else: string += '\t'
            else: 
                if datalist[each][0] == '': break  #if text is empty
                else: 
                    string += 'O'
                    if e == len(datalist[each])-1: string += '\n'
                    else: string += '\t'
            if datalist[each][0] == '.' or datalist[each][0] == '!' or datalist[each][0] == '?':
                if e == len(datalist[each])-1: string += '\n' 
                
    txt=open(path,"w") 
    txt.writelines(string) 
    txt.close() 
    
trainpath = '../Data/training/Traning'
testpath = '../Data/test_task8/Test.configuration3'


traintxtpath = './corpus/train.txt'
testtxtpath = './corpus/test.txt'

trainSetClass = construct(trainpath)
testSetClass = construct(testpath)

columnnames = ['text', 'iso']

# write data into txt files
write_txt(traintxtpath, columnnames, trainSetClass)
write_txt(testtxtpath, columnnames, testSetClass)
