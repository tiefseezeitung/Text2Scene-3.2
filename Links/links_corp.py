#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sys import exit
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
import csv
import string

def construct(path):
    """constructs a list of lists"""
    
    isoents = ['PLACE','PATH','SPATIAL_ENTITY','SPATIAL_SIGNAL',\
              'MOTION','MOTION_SIGNAL','MEASURE','NONMOTION_EVENT']
    #leave out METALINK because they are too random for the model
    isolinks = ['QSLINK', 'OLINK', 'MOVELINK', 'MEASURELINK'] 
    
    link_attr = ['trajector', 'landmark', 'trigger', 'goal', 'mover' ] 
    #attributes = ['dimensionality','form','motion_type','motion_class',\
    #              'motion_sense','semantic_type','motion_signal_type']
    
    newfile = []
    
    for subdir, dirs, files in os.walk(path):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".xml"):
                tmpfile = []
                root = ET.parse(filepath)

                t = root.find('TEXT')
                text = t.text
                doc = nlp(text)
                tree = ET.parse(filepath)
                root = tree.getroot()
                doc = nlp(root[0].text)

                prev = 1
                # this part assigns the iso entities to words in text and 
                # extracts its id
                for token in doc:
                    found = False
                    for elem in root:
                        for i in isoents:
                            for subelem in elem: 
                                if subelem.tag == i:
                                    if subelem.get('start') == str(token.idx):
                                        txt = subelem.get('text')
                                        idtxt = subelem.get('id')
                                        # split the token if it consists of 
                                        # more than one word
                                        x = txt.split(" ")
                                        for e in range(len(x)):
                                            # includes attributes:
                                            #tmpfile += [[idtxt, x[e], i]+[subelem.get(attributes[a]) for a in range(len(attributes))]]  
                                            # use this instead when you want to put a specific string if an attribute is None:
                                            #newfile += [[x[e],i]+[subelem.get(attributes[a]) if subelem.get(attributes[a])!=None  else '' for a in range(len(attributes))]] 
                                            tmpfile += [[idtxt, x[e], i]] 
                                        found = True
                                        prev = len(x)
                                        break
                    if not found: 
                        if prev > 1: prev -= 1
                        else:
                            #filter out useless data
                            txt = (str(token.text)).translate(str.maketrans('', '', string.whitespace))
                            if (txt == '' or txt == ' '): 
                                pass
                            else: 
                                # includes attributes:
                                #tmpfile += [[None, txt ,'O']+[None for n in range(len(attributes))]]
                                tmpfile += [['no_id', txt ,'O']]
                                
               # this part assigns the link attributes to our lists
                for t in range(len(tmpfile)):
                    found = False
                    tmpfile[t] += [[],[]]
                    for i in isolinks:
                        for l in root.findall('TAGS/'+i):
                            for a in link_attr:
                                if tmpfile[t][0] == l.get(a):
                                    #tmpfile[t] += [i,a]
                                    tmpfile[t][3] = tmpfile[t][3]+[i]
                                    tmpfile[t][4] = tmpfile[t][4]+[a]
                                    found = True
                    # this will only print the set of the results:
                    #tmpfile[t][3] = list(set(tmpfile[t][3]))
                    #tmpfile[t][4] = list(set(tmpfile[t][4]))
                    if not found: 
                        tmpfile[t][3] = None
                        tmpfile[t][4] = None

                    # this deletes id column:
                    #tmpfile[t] = tmpfile[t][1:]
                newfile = newfile + tmpfile
    return newfile

def writedata(path,fieldnames,datalist):
    """"writes columns and data in a csv file"""
    
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer_wl = csv.writer(csvfile, delimiter=',')
        writer.writeheader()
        for each in range(0,len(datalist)):
            if (datalist[each][1] == '.' or datalist[each][1] == '!' or datalist[each][1] == '?'):
                writer.writerow({fieldnames[f]: datalist[each][f] for f in range(len(fieldnames))})
                # adding this produces blank lines between sentences:
                writer_wl.writerow('')
            else:
                writer.writerow({fieldnames[f]: datalist[each][f] for f in range(len(fieldnames))})
     
columnnames = ['id','text', 'iso', 'link', 'role']

# construct list of lists that will later be converted to csv
trainSetClass = construct('../Data/training/Traning')
print(len(trainSetClass))

# write data into csv files
writedata('train.csv',columnnames,trainSetClass)

#test files are not provided with link tags
#testSetClass = construct('../Data/test_task8/Test.configuration3')
#print(len(testSetClass))





