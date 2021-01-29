import os
from sys import exit
import spacy
nlp = spacy.load("en_core_web_sm")
import xml.etree.ElementTree as ET
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.data_fetcher import NLPTaskDataFetcher
from flair.data import Corpus
from typing import List
from flair.embeddings import (
    TokenEmbeddings,
    WordEmbeddings,
    StackedEmbeddings,
    FlairEmbeddings,
    TransformerWordEmbeddings,
    CharacterEmbeddings,)
from flair.training_utils import EvaluationMetric
from flair.visual.training_curves import Plotter

# needed later for .txt file (but only for trial)
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


# to get iso-type
def construct(path):
    """predicts iso entity"""
    # create string that will be converted to txt file later
    newfile = ''
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
                                        for e in range(0,len(x)):
                                                newfile += x[e] +' '+i+'\n'
                                                #csv would be
                                                #newfile += x[e] +','+i+'\n'
                                        found = True
                                        break
                    if not found: 
                        #filter out useless data
                        if token.text == ('\n' or'' or ' ' or '\n\n\n' or '\n\n'): pass
                        else: 
                            newfile += token.text +' O\n'
                            #csv:
                            #newfile += token.text +',O\n'
                #print(newfile)
    return newfile


trainpath = '/Data/training/Traning'
trialpath = '/Data/spaceeval_trial_data/spaceeval_trial_data'
testpath = '/Data/test_task8S'

traintxtpath = '/corpus/t.txt'
trialtxtpath = 'corpus/trial.txt'
testtxtpath = '/corpus/test.txt'
# this is the folder in which train, test and dev files reside
data_folder = '/corpus'

trialLst = constructtrial(trialpath) # dev = trial
trainSetClass = construct(trainpath)
testSetClass = construct(testpath)


# write .txt files
traintxt = open(traintxtpath, "w", encoding="utf-8")
traintxt.write(trainSetClass)
traintxt.close()
#print(trainSetClass)
testtxt = open(testtxtpath, "w", encoding="utf-8")
testtxt.write(testSetClass)
testtxt.close()


trialtxt = open(trialtxtpath, "w", encoding="utf-8")
#trialtxt.write(trialLst)
#trialtxt.close()
#exit()

#newlist
for each in trialLst:
    l = str(each)
    trialtxt.write(l)
    trialtxt.write("\n")
trialtxt.close()
print("")

# 1.erst keine empty lines
# 2.remove lines with no text
# 3.remove lines with no text but with entity
# 4.add empty lines at the end of a sentence

# 1
traintxt = open(traintxtpath, "w")
lines = trainSetClass.split("\n")
non_empty_lines = [line for line in lines if line.strip() != ""]
trainSetClass_without_empty_lines = ""
for line in non_empty_lines:
      trainSetClass_without_empty_lines += line + "\n"
traintxt.write(trainSetClass_without_empty_lines)

# 2.-3. 
with open(traintxtpath, "r") as traintxt:
    lines = traintxt.readlines()
with open(traintxtpath, "w") as traintxt:
    for line in lines:
        if line.strip("\n") != "         O":
            if line.strip("\n") != " PATH" and line.strip("\n") != " PLACE" \
                and line.strip("\n") != " SPATIAL_SIGNAL" and line.strip("\n")\
                    != " MOTION_SIGNAL" and \
                        line.strip("\n") != " SPATIAL_ENTITY" and \
                            line.strip("\n") != " LOCATION" \
                                and line.strip("\n") != " MEASURE" and \
                                    line.strip("\n") != " MOTION" and \
                                        line.strip("\n") != " NONMOTION_EVENT":
                traintxt.write(line)

# 4.
# https://www.quora.com/How-do-you-write-in-a-new-line-on-a-text-file-in-Python (24.01.2021)
#We read the existing text from file in READ mode 
traintxt=open(traintxtpath,"r") 
fline="\n"    #Prepending string  newly added FIRST LINE\n
oline=traintxt.readlines() 
#Here, we prepend the string we want to on first line 
lst = []
for end in range(0,len(oline)):
    if oline[end]==". O\n" or oline[end]=="! O\n" or oline[end]=="? O\n":
        lst+=[end]
lst.reverse()
for each in lst:
    oline.insert(each+1,fline)
traintxt.close() 
#We again open the file in WRITE mode  
traintxt=open(traintxtpath,"w") 
traintxt.writelines(oline) 
traintxt.close() 



testtxt = open(testtxtpath, "w")
lines = testSetClass.split("\n")
non_empty_lines = [line for line in lines if line.strip() != ""]
testSetClass_without_empty_lines = ""
for line in non_empty_lines:
      testSetClass_without_empty_lines += line + "\n"
testtxt.write(testSetClass_without_empty_lines)

# 2.-3. 
with open(testtxtpath, "r") as testtxt:
    lines = testtxt.readlines()
with open(testtxtpath, "w") as testtxt:
    for line in lines:
        if line.strip("\n") != "         O":
            if line.strip("\n") != " PATH" and line.strip("\n") != " PLACE" and line.strip("\n") != " SPATIAL_SIGNAL" and line.strip("\n") != " MOTION_SIGNAL" and line.strip("\n") != " SPATIAL_ENTITY" and line.strip("\n") != " LOCATION" and line.strip("\n") != " MEASURE" and line.strip("\n") != " MOTION" and line.strip("\n") != " NONMOTION_EVENT":
                testtxt.write(line)
4.
# https://www.quora.com/How-do-you-write-in-a-new-line-on-a-text-file-in-Python (24.01.2021)
#We read the existing text from file in READ mode 
testtxt=open(testtxtpath,"r") 
fline="\n"    #Prepending string  newly added FIRST LINE\n
oline=testtxt.readlines() 
#print(oline)
#Here, we prepend the string we want to on first line 
lst = []
for end in range(len(oline)):
    if oline[end]==". O\n" or oline[end]=="! O\n" or oline[end]=="? O\n":
        lst+=[end]
lst.reverse()
for each in lst:
    oline.insert(each+1,fline)
testtxt.close() 
#We again open the file in WRITE mode  
testtxt=open(testtxtpath,"w") 
testtxt.writelines(oline) 
testtxt.close()


trialtxt = open(trialtxtpath, "w")
for each in trialLst:
    l = str(each)
    trialtxt.write(l)
    trialtxt.write("\n")
trialtxt.close()
print("")



from flair.data import Corpus
# from flair.datasets import ClassificationCorpus doesnt work with this
from flair.datasets import ColumnCorpus

# define columns
columns = {0: 'text', 1: 'iso'}

# load corpus containing training, test and dev data
corpus: Corpus = ColumnCorpus(data_folder, columns,
                                      test_file='test.txt',
                                      dev_file='trial.txt',  
                                      train_file='train.txt')
print(corpus)

# 2. what tag do we want to predict?
tag_type = "iso"


# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)

# initialize embeddings
embedding_types: List[TokenEmbeddings] = [
    WordEmbeddings("glove"),
    #TransformerWordEmbeddings('distilbert-base-uncased', fine_tune=True),
    # comment in this line to use character embeddings
    # CharacterEmbeddings(),
    # comment in these lines to use contextual string embeddings
    #
    # FlairEmbeddings('news-forward'),
    #
    # FlairEmbeddings('news-backward'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(
    hidden_size=256,
    embeddings=embeddings,
    tag_dictionary=tag_dictionary,
    tag_type=tag_type,
    use_crf=True,
)

# initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

trainer.train(
    "resources/taggers/example-iso",
    learning_rate=0.1,
    mini_batch_size=32,
    max_epochs=5,
    shuffle=False,
)

plotter = Plotter()
plotter.plot_training_curves("resources/taggers/example-iso/loss.tsv")
plotter.plot_weights("resources/taggers/example-iso/weights.txt")

