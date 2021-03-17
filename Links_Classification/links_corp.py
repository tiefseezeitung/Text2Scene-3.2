#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sys import exit
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
import csv
import string


def construct(path, link):
    """constructs a list of lists with entries text, iso entity,semantic type
    and the relation (if token is the trigger)"""
    
    isoents = ['PLACE','PATH','SPATIAL_ENTITY','SPATIAL_SIGNAL',\
              'MOTION','MOTION_SIGNAL','MEASURE','NONMOTION_EVENT']
    
    isolink = link
    if isolink == 'QSLINK': sem_type = 'TOPOLOGICAL'
    elif  isolink == 'OLINK': sem_type = 'DIRECTIONAL'

    newfile = []
    
    def toword(idtr,idlst):
        'returns text of an id'
        for i in idlst:
            if i[0] == idtr:
                return i[1]
            
    def toidrole(idtr,rllst):
        '''returns trajector,landmark,from and to id'''
        found = False
        for i in rllst:
            if i[0] == idtr:
                found = True
                return i[1],i[2],i[3],i[4]
        if found == False:
            return None, None, None, None
            
    # walk through given directory
    for subdir, dirs, files in os.walk(path):
        newfile = []
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


                # make list of all entities:
                idfile = []
                for elem in root:
                    for i in isoents:
                        for subelem in elem: 
                            if subelem.tag == i:
                                txt = subelem.get('text')
                                idtxt = subelem.get('id')
                                idfile += [[idtxt, txt, subelem.get('start'), subelem.get('semantic_type')]]
                                
                #make list of all entries of link
                rolefile = []
                for elem in root:
                        for subelem in elem: 
                            if subelem.tag == isolink:
                                rolefile += [[subelem.get('trigger'),subelem.get('trajector'),subelem.get('landmark'),subelem.get('fromID'),subelem.get('toID')]]
                
                # this part assigns the iso entities, semantic_types, relation to words in text
                prev = 1
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
                                        
                                        if subelem.get('semantic_type') == sem_type:
                                            traj, lm, fromid, toid = toidrole(idtxt,
                                                                rolefile)
                                            if traj == None or lm == None: #link not complete
                                                for e in range(len(x)):
                                                    newfile += [[x[e], i, 'O', 'O']]    
                                            else: #means all roles available (link complete)
        
                                                if traj == fromid:
                                                    for e in range(len(x)):
                                                        newfile += [[x[e], i, subelem.get('semantic_type'), isolink+'(arg1=trajector,arg2=landmark)' ]] 
                                                elif traj == toid:
                                                    for e in range(len(x)):
                                                        newfile += [[x[e], i, subelem.get('semantic_type'), isolink+'(arg1=landmark,arg2=trajector)' ]]    
                                                else: 
                                                    print('false data')
                                                    for e in range(len(x)):
                                                        newfile += [[x[e], i, 'O', 'O']]    
                  
                                        else:
                                            for e in range(len(x)):
                                                x[e] = (str(x[e])).translate(str.maketrans('', '', string.whitespace))
                                                if x[e] == '': pass
                                                else: newfile += [[x[e], i]+[subelem.get('semantic_type') if (subelem.get('semantic_type') != None and subelem.get('semantic_type') != '') else 'O']+['O']]    
                                        
                                        found = True
                                        prev = len(x)
                                        break
                    if not found: 
                        if prev > 1: prev -= 1
                        else:
                            #filter out useless data
                            txt = (str(token.text)).translate(str.maketrans('', '', string.whitespace))
                            x = txt.split(' ')
                            for e in range(len(x)):
                                if (x[e] == '' or x[e] == ' '): 
                                    pass
                                else: 
                                    newfile += [[x[e], 'O' , 'O', 'O']]    
    return newfile

# not used, we use writetxt
def writecsv(path,fieldnames,datalist):
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

def writetxt(path,fieldnames,datalist):
    """"writes columns and data in a txt file"""
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

#choose either qslink or olink
#link = 'QSLINK'
link = 'OLINK'

columnnames = ['text', 'iso', 'semantic_type', link]
trainSetClass = construct('../Data/training/Traning', link)
writetxt('train_'+link+'.txt',columnnames,trainSetClass)