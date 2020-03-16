'''
Given two or more models, compare their performance and evaluate which is best

NEED: model.json model.h5 (using these files, we reconstruct the model)
      x_test y_test (x_test is passed into the model to get predictions this is then compared to y_test to generate f_score)
      dictionary (enumerate the words)
      targets (enumerate the tags)

step1: recrete the model
step2: make prediction using x_test
step3: get f_score


THERE WILL BE ONE X_TEST Y_TEST BUT MULTIPLE MODELS
- the modelFiles are stored in sub-directories
    <example>
    extraction/model/models >> re3d >> modelName1, modelName2

what will be passed is modelName
'''

import tensorflow as tf
from tensorflow.keras.models import model_from_json
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report
import json


class CrossValidator:

    def __init__(self, dataset, model_group, model_names):
        self.dataset = dataset
        self.model_group = model_group
        self.model_names = model_names

    def pred2label(self, pred):
        out = []
        for pred_i in pred:
            out_i = []
            for p in pred_i:
                p_i = np.argmax(p)
                out_i.append(self.dataset.categories[p_i].replace("xxxPADDINGxxx", "O"))
            out.append(out_i)
        return out
    def test2label(self, pred):
        out = []
        for pred_i in pred:
            out_i = []
            for p in pred_i:
                out_i.append(self.dataset.categories[p].replace("xxxPADDINGxxx", "O"))
            out.append(out_i)
        return out

    # def script():
    #     for layers in range(10) # this is inputSize:
    #         layersSize = layers*10
            # run LSTM with layersSize
            # save f1 score in arr1
            # if the next 2 f1 score is decreasing, stop
            # findMax(arr1) = [a,b,c,d,max,e,f,g]
            # compare the d and the e, and if e> d => layersSize is between max and e.
            # repeat this between layersSize of max and e
            # stop as soon as 2 of the f1 decrease
        # let inputSize = N
        #  For this one, you run the model N/10 + 10
        # for the k-fold, you run it k times
        # so in total it is k(N/10 + 10)

    def compare(self):

        f_scores = []
        max_fscore = 0
        max_index = -666
        for mn in self.model_names:
            folder_path = 'extraction/model/models/' + self.model_group + '/' + mn
            # folder_path = 'models/' + self.model_group + '/' + mn
            model_file_path = folder_path + '/Model.json'
            weights_file_path = folder_path + '/ModelWeights.h5'

            with open(model_file_path) as model_file:
                loaded_model_json = model_file.read()
            model_file.close()

            loaded_model = tf.keras.models.model_from_json(loaded_model_json)
            loaded_model.load_weights(weights_file_path)

            #model has been loaded now make prediction for all x_test
            pred = loaded_model.predict( [self.dataset.x_test] , verbose = 1)


            #change the categorical y values into int (bcoz the predictions passed by the models is int. Also )
            # Y_TEST = np.array(self.dataset.y_test)
            sent = []
            for j in np.array(self.dataset.y_test):
                for k in j:
                    for l in range(len(k)):
                        if(k[l] > 0):
                            sent.append(l)
            new_ytest = []
            temp = []
            count = 1
            for i in sent:
                if count <= self.dataset.max_len:
                    temp.append(i)
                else:
                    new_ytest.append(temp)
                    temp = []
                    temp.append(i)
                    count = 1
                count = count + 1

            pred_labels = self.pred2label(pred)
            test_labels = self.test2label(new_ytest)

            fscore = float( f1_score(test_labels, pred_labels) )

            f_scores.append( fscore )
            print("Analyzing model: " + str(mn))
            print("f_score: ", fscore)
            print()

        for i in range( len(f_scores) ):
            if f_scores[i] > max_fscore:
                max_fscore = f_scores[i]
                max_index = i

        #to change the epochs
        #REMOVE this if statement when not crossvalidating thru optimizer
        if max_fscore == 0.0:
            max_index = 1

        return self.model_names[max_index]
