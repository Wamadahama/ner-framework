import nltk
from nltk.corpus.reader import *
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences 
from tensorflow.keras.utils import to_categorical

class DataHandler:
    def __init__(self, filePath):
        self.filePath = filePath

        temp = filePath.split('.')
        self.fileType = temp[len(temp)-1]

        folders = self.filePath.split('/')
        root = ''
        for i in range( len(folders)-1 ):
            root += folders[i] + '/'
            self.root = root
            self.fileName = folders[i+1]



    def getSentences(self):
        if self.fileType == 'csv':
            df = pd.read_csv(self.filePath, header=None, na_values='')

            sentences = []
            sent = []
            for index, row in df.iterrows():
                if pd.isnull(row[0]):
                    sentences.append(sent)
                    sent = []
                else:
                    (word, tag) = (row[0], row[1])
                    sent.append( (word, tag) )
            return sentences
        #works for conll, txt
        else:
            content = ConllCorpusReader(self.root,
                                        self.fileName,
                                        ['words', 'pos'])
            return content.tagged_sents()



    def get_train_test(self, sentences, test_size, max_len=None):
        if max_len is None:
            max_len = max(len(sen) for sen in sentences)
        X = []
        padded_sent = []
        x_index = 0
        for s in sentences:
            for i in range(max_len):
                if i >= len(s):
                    padded_sent.append("xxxPADDINGxxx")
                else:
                    padded_sent.append(s[i][0])

            X.append(padded_sent)
            padded_sent = []
        #print (len(X[53]))
        ##print(X[53])
        new_sentences = X

        words = []
        for s in X:
            for w in s:
                words.append(w)
        unique_words = list(set(words))
        num_words = len(unique_words)
        self.n_words = num_words

        words2index = { w: i for i,w in enumerate(unique_words) }
        X = [[words2index[w] for w in s] for s in X]

        self.vocabulary = words2index

        #print(sentences)
        tags = []
        for s in sentences:
            for w in s:
                tags.append(w[1])
        tags = list(set(tags))
        num_tags = len(tags)
        self.n_tags = num_tags

        tags2index = { t: i for i,t in enumerate(tags) }
        self.tags = tags2index 
        #print("")
        #print(tags)
        #print("")
        y = [[tags2index[w[1]] for w in s] for s in sentences]
        y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=tags2index["O"])
        y = [to_categorical(i, num_classes=num_tags) for i in y]

        X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X,y, test_size=test_size)
        return X_TRAIN, X_TEST, Y_TRAIN, Y_TEST


    def get_dataset(self):
        sentences = self.getSentences() 
        max_len = max([len(sentence) for sentence in sentences])
        X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = self.get_train_test(sentences=sentences, test_size=0.1, max_len=max_len)
        return Dataset(X_TRAIN, X_TEST, Y_TRAIN, Y_TEST, max_len, self.n_words, self.n_tags, self.vocabulary, self.tags)
    

class Dataset:
    def __init__(self, x_train, x_test, y_train, y_test, max_len, n_words, n_tags, vocabulary, tags):
        self.x_train    = x_train
        self.x_test     = x_test
        self.y_train    = y_train
        self.max_len    = max_len
        self.n_words    = n_words 
        self.n_tags     = n_tags
        self.vocabulary = vocabulary
        self.tags       = tags 
