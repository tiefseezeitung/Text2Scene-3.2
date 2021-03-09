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
from flair.datasets import ColumnCorpus

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
    #WordEmbeddings("glove"),
    TransformerWordEmbeddings('distilbert-base-uncased', fine_tune=True),
    # comment in this line to use character embeddings
    # CharacterEmbeddings(),
    # comment in these lines to use contextual string embeddings
    #
    # FlairEmbeddings('news-forward'),
    #
    # FlairEmbeddings('news-backward'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

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
    "resources2/taggers/example-iso",
    learning_rate=0.5,
    mini_batch_size=32,
    max_epochs=3,
)

# not necessary, but plots learning curves
plotter = Plotter()
plotter.plot_training_curves("resources/taggers/example-iso/loss.tsv")
plotter.plot_weights("resources/taggers/example-iso/weights.txt")

