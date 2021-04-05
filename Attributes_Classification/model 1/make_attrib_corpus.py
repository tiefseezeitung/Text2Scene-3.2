#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
import csv
import string

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
                                        x = txt.split(" ")
                                        for e in range(len(x)):
                                            x[e] = (str(x[e]).translate(str.maketrans('', '', string.whitespace)))
                                            if x[e] != '':
                                                # add line as a list
                                                newfile += [[x[e],i]+[subelem.get(attributes[a]) if (subelem.get(attributes[a])!=None and subelem.get(attributes[a])!='') else 'O' for a in range(len(attributes))]]
                                        found = True
                                        prev = len(x)
                                        break
                    if not found: 
                        # if last tagged word was longer than one token, 
                        # skip next token because it is already in our list
                        if prev > 1: prev -= 1
                        
                        # if word/token not tagged, add word and list of O's 
                        # to list
                        else:
                            #filter out useless data
                            txt = (str(token.text)).translate(str.maketrans('', '', string.whitespace))
                            if (txt == ''): 
                                pass
                            else: 
                                newfile += [[txt ,'O']+['O' for n in range(len(attributes))]]
    return newfile

def write_csv(path,fieldnames,datalist):
    """"Writes data in columns into a csv file, columns separated by ','"""
    
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer_wl = csv.writer(csvfile, delimiter=',')
        writer.writeheader()
        for each in range(0,len(datalist)):
            if (datalist[each][0] == '.' or datalist[each][0] == '!' or datalist[each][0] == '?'):
                writer.writerow({fieldnames[f]: datalist[each][f] for f in range(len(fieldnames))})
                # adding this produces blank lines between sentences (for flair sentence recognition)
                writer_wl.writerow('')
            else:
                writer.writerow({fieldnames[f]: datalist[each][f] for f in range(len(fieldnames))})
                
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
            
            
attributes = ['dimensionality','form','motion_type','motion_class',\
              'motion_sense','semantic_type','motion_signal_type']
columnnames = ['text', 'iso'] + attributes

# construct list of lists that will later be converted to txt file
trainSetClass = construct(attributes,'../../Data/training/Traning')
testSetClass = construct(attributes,'../../Data/test_task8/Test.configuration3')


# write data into txt files
write_txt('train.txt',columnnames,trainSetClass)
write_txt('test.txt',columnnames,testSetClass)