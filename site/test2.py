from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator
from extraction.model.optimize import Optimizer
from threading import Thread
import time

def timer():
    pass

def main():
    # Test Model training:

#from dataset import DataHandler
    #d_set1 = DataHandler('../../../nlp-model/dataset/MITMovie_dataset.csv')
    #sentences = d_set1.getSentences()
    #X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = d_set1.get_train_test(sentences=sentences, test_size=0.1, max_len=30)

    loader  = DataHandler("extraction/datasets/MITMovie_dataset.csv")
    dataset = loader.get_dataset()

                            #rest is always fixed
    optimalModel = Optimizer(dataset, initialUnits = 224, initialEpochs = 6).getOptimizedModel()




    # num_units = 256
    # num_epochs = 1
    # initial_model = BiLstm("movie001", "movie", dataset, (0,0), num_units, 0.1, 0.1, 100, 32, num_epochs)
    # trainer = ModelTrainer()
    # initial_trained_model = trainer.train(initial_model, dataset)
    #
    #
    # iter = 1
    # while True:
    #     units_name = "movie_units"+str(iter)
    #     training_model1 = BiLstm(units_name, "movie", dataset, (0,0), num_units+256, 0.1, 0.1, 100, 32, num_epochs)
    #     trainer = ModelTrainer()
    #     trained_model = trainer.train(training_model1, dataset)
    #
    #     epochs_name = "movie_epochs"+str(iter)
    #     training_model2 = BiLstm(epochs_name, "movie", dataset, (0,0), num_units, 0.1, 0.1, 100, 32, num_epochs+1)
    #     trainer = ModelTrainer()
    #     trained_model = trainer.train(training_model2, dataset)
    #
    #     if iter == 1:
    #         best_model = CrossValidator(dataset, "movie", ["movie001", units_name, epochs_name]).compare()
    #
    #     else:
    #         best_model = CrossValidator(dataset, "movie", [units_name, epochs_name]).compare()
    #
    #     if best_model == "movie001":
    #         print("Initial model was the best model")
    #         break
    #     elif best_model == units_name:
    #         num_units += 256
    #         print("No. of units now changed to: ", num_units)
    #     else:
    #         num_epochs += 1
    #         print("No. of epochs now changed to: ", num_epochs)



# units:76      f_score:  0.09864116758933064
# units:256     f_score:  0.101530240466359
# units:512     f_score:  0.10778164924506389
# units:1024    f_score:  0.10430009149130832
# units:2048    f_score:  0.060784313725490195
# units:4096    f_score:  0.0

# Training with units: 768 epochs: 6
# f_score:  0.6251036312386006

# Training with units: 160 epochs: 5
# f_score:  0.5772357723577236



main()
