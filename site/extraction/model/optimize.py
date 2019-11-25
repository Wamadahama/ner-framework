from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator
from threading import Thread
import time

    # training_model = BiLstm("movie3", "movie", dataset, (0,0), 1024, 0.1, 0.1, 100, 32, 1)
    # trainer1 = ModelTrainer()
    # trainer.train(training_model, dataset)



class Optimizer:
    def __init__(self, model):
        self.model = model

    def thread_changeUnits(self):
        pass



    def getOptimizedModel(self):

        trainer = ModelTrainer()



        #starting points
        num_units = self.model.lstm_units
        num_epochs = self.model.epochs
        iter = 1
        while True:
            #change the no. of units
            #change the no. of epochs
            #see which produces better result and repeat
            # timeout = time.time() + 60*60   #stop after an hour


            thread = Thread(target = thread_changeUnits, args = ())
            thread.start()
            thread.join()


                                  #<dataset,  group     model1    model2>
        best_model = CrossValidator(dataset, 'movie', ['movie3', 'movie4', 'movie5']).compare()
        print(best_model, " was determined to be the best model")
        # best_model = crossvaldation(model1, model2) #where model1 and model2 are instances of 'model class'
