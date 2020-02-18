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
