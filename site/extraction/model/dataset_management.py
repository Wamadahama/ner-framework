import nltk
from nltk.corpus.reader import *
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split



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
                                      ['pos', 'words'])
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
        print (len(X[53]))
        print(X[53])
        new_sentences = X

        words = []
        for s in X:
            for w in s:
                words.append(w)
        unique_words = list(set(words))
        num_words = len(unique_words)

        words2index = { w: i for i,w in enumerate(unique_words) }
        X = [[words2index[w] for w in s] for s in X]

        tags = []
        for s in sentences:
            for w in s:
                tags.append(w[1])
        tags = list(set(tags))
        num_tags = len(tags)

        tags2index = { t: i for i,t in enumerate(tags) }
        print(tags2index)
        print()
        # y = [[tags2index[w[1]] for w in s] for s in sentences]

        # y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=tags2index["O"])

        y = []
        padded_sent = []
        x_index = 0
        for s in sentences:
            for i in range(max_len):
                if i >= len(s):
                    padded_sent.append( tags2index[ 'O' ] )
                else:
                    padded_sent.append( tags2index[ s[i][1] ] )

            y.append(padded_sent)
            padded_sent = []


        X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X,y, test_size=test_size)
        return X_TRAIN, X_TEST, Y_TRAIN, Y_TEST
