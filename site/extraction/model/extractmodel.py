import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model, load_model, model_from_json
from ..util.models import *
from ..util.file import read_json


class ExtractionModel:
    """Loads existing models and provides methods like predict to use them"""
    def __init__(self, model_name=None, algorithm="bi-lstm", models_path="extraction/model/models/"):

        if model_name == None or model_name == "":
            self.model_name = model_name
            self.models_path = models_path
        else:
            self.model_name = model_name
            self.models_path = models_path
            self.load_pretrained_model(model_name)

        self.algorithm  = algorithm

    def load_pretrained_model(self, model_name=None):
        """
        Loads a pre trained model from the models/ directory 
        The models/ directory has the following strcuture

           
           models/
           +-- model1/
               /Dataset/            -> Raw tagged dataset used to train the model's weights 
               +-- ModelWeights.h5  -> Weights of the trained model  
               +-- Model.json       -> Definition of the model
               +-- Vocabulary.json  -> Mapping of the words used in the model to numerical values 

           ...
           +-- modelN/ 
        """

        # load the model architecture 
        if self.model_name == None:
            self.model_name = model_name
        
        model_files = read_model_files(self.models_path + self.model_name)

        # Read the vocabulary, 
        vocab_file = [file for file in model_files if "Vocabulary.json" in file][0]
        # TODO: optimize this down to one call
        self.vocabulary = read_json(vocab_file, output='pairs-list')
        self.vocabulary_with_index = read_json(vocab_file, output='dict')

        #if "ENDPAD" not in self.vocabulary:
        #    key = len(self.vocabulary)+1
        #    self.vocabulary.update({ "ENDPAD": key})

        # read the categories
        categories_file = [file for file in model_files if "Categories.json" in file][0]
        self.categories = read_json(categories_file, output='dict')["categories"]

        # Read the load the model and weights
        model_file = [file for file in model_files if "Model.json" in file][0]
        print("Attempting to load model {}".format(model_file))

        try:
            self.model_file = model_file 
            self.Model = model_from_json(read_json(model_file, output='json'))
            self.Model.load_weights([file for file in model_files if "ModelWeights.h5" in file][0])
            print("Done loading model")
        except:
            print("Unable to load model")
            return
        

        

    #TODO: deal with punctuation (better split)
    def extract(self, text):
        """ Given a text return the extractions. Uses the model loaded in the self.load_pretrianed_model """
        # prepare text
        text = text.lower().split(' ')

        # add end padding to the vector
        for i in range(self.Model.layers[0].output_shape[0][1]): # [(n, m)]
            if i >= len(text):
                text.append("xxxPADDINGxxx")

        # words to numbers 
        input_vector = []
        for word in text:
            if word in self.vocabulary:
                input_vector.append(self.vocabulary[word])
            else:
                input_vector.append(self.vocabulary["xxxPADDINGxxx"])

        # perform extraction
        prediction = self.Model.predict(np.array([input_vector]))
        #print(prediction)
        prediction = np.argmax(prediction, axis=-1)
        #print(prediction)

        print("{:14} ({:5}): {}".format("Word", "True", "Pred"))
        for w,pred in zip(input_vector, prediction[0]): 
            for pair in self.vocabulary_with_index:
                if(w == pair["index"]):
                    word = pair['word']

                    if pred > 25:
                        pred = 5
                    
                    category = self.categories[pred]
                    print("{:14}: {}".format(word,category))
