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

def writetxt(path,fieldnames,datalist):
    """"writes columns and data in a csv file"""
    string = ''
    for each in range(0,len(datalist)):
        # eine zeile
        for e in range(len(datalist[each])):
            # spalte
            #print(e)
            if datalist[each][e] != None:
                string+= str(datalist[each][e])
                if e == len(datalist[each])-1: string += '\n'
                else: string += '\t'
            else: 
                if datalist[each][0] == '': break  #if text is empty
                else: 
                    string += 'None'
                    if e == len(datalist[each])-1: string += '\n'
                    else: string += '\t'
            if datalist[each][0] == '.' or datalist[each][0] == '!' or datalist[each][0] == '?':
                if e == len(datalist[each])-1: string += '\n' 
                #string += ' '
    txt=open(path,"w") 
    txt.writelines(string) 
    txt.close() 

    # hier müssten noch die leeren zeilen eingefügt werden,
    # damit das ende eine satzes erkannt wird
    
    
        
    

attributes = ['dimensionality','form','motion_type','motion_class',\
              'motion_sense','semantic_type','motion_signal_type']
columnnames = ['text', 'iso'] + attributes

# construct list of lists that will later be converted to csv
#trialLst = constructtrial('../Data/spaceeval_trial_data') # dev = trial
trainSetClass = construct(attributes,'../Data/training/Traning')
testSetClass = construct(attributes,'../Data/test_task8/Test.configuration3')
print(len(trainSetClass))
print(len(testSetClass))

# write data into csv files
writetxt('train_new.txt',columnnames,trainSetClass)
writetxt('test_new.txt',columnnames,testSetClass)


