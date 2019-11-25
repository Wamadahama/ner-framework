import numpy as np
import os
import json
from keras import backend as K

class ModelTrainer:
    """Class for training a NER model"""
    def __init__(self, model=None, dataset=None):
        self.model = model
        self.dataset = dataset

    # def recall_m(self, y_true, y_pred):
    #     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    #     possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    #     recall = true_positives / (possible_positives + K.epsilon())
    #     return recall
    #
    # def precision_m(self, y_true, y_pred):
    #     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    #     predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    #     precision = true_positives / (predicted_positives + K.epsilon())
    #     return precision
    #
    # def f1_m(self, y_true, y_pred):
    #     precision = precision_m(y_true, y_pred)
    #     recall = recall_m(y_true, y_pred)
    #     return 2*((precision*recall)/(precision+recall+K.epsilon()))

    def train(self, model, dataset):
        try:
            # Get the layers of the model and then train
            print("Training with units: " + str(model.lstm_units) + " epochs: " + str(model.epochs))
            model_layout = model.get_model()
            model_layout.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
            model_layout.fit(np.array(dataset.x_train), np.array(dataset.y_train), validation_split=0.1,
                             batch_size=model.batch_size, epochs=model.epochs)

            self.save_model(model, model_layout, dataset) # store the trained model to disk

            return model_layout
        except Exception as e:
            print(e)
            print("Unable to train model")


    def save_model(self, model_info, trained_model, dataset):
        """
        Need to save the following files
               +-- ModelWeights.h5  -> Weights of the trained model
               +-- Model.json       -> Definition of the model
               +-- Vocabulary.json  -> Mapping of the words used in the model to numerical values
        """
        save_dir = "extraction/model/models/" + model_info.group + "/" + model_info.name + "/"
        print("saving to " + save_dir)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)



        model_json = trained_model.to_json()
        with open(save_dir+"Model.json", "w") as json_file:
            json_file.write(model_json)
        trained_model.save_weights(save_dir + "ModelWeights.h5")

        vocab_list = []
        for word,index in dataset.dictionary.items():
            dict_item = {}
            dict_item["word"] = word
            dict_item["index"] = index
            vocab_list.append(dict_item)

        vocab_json = json.dumps(vocab_list)

        tags = json.dumps({"categories": list(dataset.categories)})

        with open(save_dir+"Vocabulary.json", "w") as vocab_file:
            vocab_file.write(vocab_json)

        with open(save_dir+"Categories.json", "w") as tags_file:
            tags_file.write(tags)
