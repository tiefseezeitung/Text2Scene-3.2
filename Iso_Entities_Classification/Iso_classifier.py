from flair.models import SequenceTagger
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from typing import List
from flair.embeddings import (
    TokenEmbeddings,
    WordEmbeddings,
    StackedEmbeddings,
    FlairEmbeddings,
    TransformerWordEmbeddings,
    CharacterEmbeddings,)
from flair.visual.training_curves import Plotter
from flair.training_utils import EvaluationMetric

# this is the folder in which train, test and dev files reside
data_folder = './corpus'

# define columns
columns = {0: 'text', 1: 'iso'}

# load corpus containing training, test and dev data
corpus: Corpus = ColumnCorpus(data_folder, columns,
                                      test_file='test.txt', 
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
    FlairEmbeddings('news-forward-fast'),
    #
    FlairEmbeddings('news-backward-fast'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

tagger: SequenceTagger = SequenceTagger(
    hidden_size=128,
    embeddings=embeddings,
    tag_dictionary=tag_dictionary,
    tag_type=tag_type,
    use_crf=True, rnn_layers=2,
)

# initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

# the folder where your model, log files etc will be saved to
model_path = "resources/taggers/iso_x"

trainer.train(
    model_path,
    learning_rate=0.15,
    mini_batch_size=8,
    max_epochs=15,
    write_weights=True,
    checkpoint=True
)

# plots learning curves (creates png plot) | not necessary for training
plotter = Plotter()
plotter.plot_training_curves(model_path+"/loss.tsv")
plotter.plot_weights(model_path+"/weights.txt")


# in case you want to stop training and want to continue at another time, 
# just load the checkpoint with following code:
'''   
checkpoint = model_path+"/checkpoint.pt"
trainer = ModelTrainer.load_checkpoint(checkpoint, corpus)
trainer.train(
    model_path,
    learning_rate=0.15,
    mini_batch_size=8,
    max_epochs=12,
    write_weights=True,
    checkpoint=True
)
'''
