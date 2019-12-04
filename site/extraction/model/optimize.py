from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm, BiLstm_2layers
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator
import threading
import time

    # training_model = BiLstm("movie3", "movie", dataset, (0,0), 1024, 0.1, 0.1, 100, 32, 1)
    # trainer1 = ModelTrainer()
    # trainer.train(training_model, dataset)



class Optimizer:
    def __init__(self, dataset, initialUnits, initialEpochs):
        self.dataset = dataset
        self.num_units = initialUnits
        self.num_epochs = initialEpochs

    def thread_changeUnits(self, iter, dataset, num_units, num_epochs):
        units_name = "movie_units"+str(iter)
        num_units += 64
        training_model1 = BiLstm(units_name, "movie", dataset, (0,0), num_units, 0.1, 0.1, 100, 32, num_epochs)
        # training_model1 = BiLstm_2layers(units_name, "movie", dataset, (0,0), 160, num_units, 0.1, 0.1, 100, 32, num_epochs)
        trainer = ModelTrainer()
        trained_model = trainer.train(training_model1, dataset)

        # return units_name

    def thread_changeEpochs(self, iter, dataset, num_units, num_epochs):
        epochs_name = "movie_epochs"+str(iter)
        num_epochs += 1
        training_model2 = BiLstm(epochs_name, "movie", dataset, (0,0), num_units, 0.1, 0.1, 100, 32, num_epochs)
        # training_model2 = BiLstm_2layers(epochs_name, "movie", dataset, (0,0), 160, num_units, 0.1, 0.1, 100, 32, num_epochs)
        trainer = ModelTrainer()
        trained_model = trainer.train(training_model2, dataset)


    def getOptimizedModel(self):
        iter = 1
        while True:
            t1 = threading.Thread(target=self.thread_changeUnits, args=(iter, self.dataset, self.num_units, self.num_epochs,))
            t2 = threading.Thread(target=self.thread_changeEpochs, args=(iter, self.dataset, self.num_units, self.num_epochs,))

            t1.start()
            t2.start()

            t1.join()
            t2.join()


            units_name = "movie_units"+str(iter)
            epochs_name = "movie_epochs"+str(iter)

            best_model = CrossValidator(self.dataset, "movie", [units_name, epochs_name]).compare()

            if best_model == units_name:
                self.num_units += 64
                print("No. of units now changed to: ", self.num_units)
            else:
                self.num_epochs += 1
                print("No. of epochs now changed to: ", self.num_epochs)

            iter += 1
