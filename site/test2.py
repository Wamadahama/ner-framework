from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm, BiLstmCRF, BiLstm_2layers, BiLstm_nlayers
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator
from extraction.model.optimize import Optimizer
from threading import Thread
import time


def main():
    # Test Model training:

#from dataset import DataHandler
    #d_set1 = DataHandler('../../../nlp-model/dataset/MITMovie_dataset.csv')
    #sentences = d_set1.getSentences()
    #X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = d_set1.get_train_test(sentences=sentences, test_size=0.1, max_len=30)
    loader  = DataHandler("extraction/datasets/re3d_dataset.txt")
    dataset = loader.get_dataset()

    print(dataset)
                            #rest is always fixed
    # optimalModel = Optimizer(dataset, modelgroup="re3d", initialUnits = 224, initialEpochs = 6).getOptimizedModel() #TODO: modelname and modelGroup should be dynamic

# Training with units: 352 epochs: 11


    num_units = 216
    num_epochs = 2
    num_layers = 4
    initial_model = BiLstm_nlayers("movie001", "movie", dataset, (0,0), num_units, num_layers, 0.1, 0.1, 70, 64, num_epochs)
    trainer = ModelTrainer()
    initial_trained_model = trainer.train(initial_model, dataset)


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



####################################################
###                    MOVIE                     ###
###  Training with units: 160 epochs: 5          ###
###  f_score:  0.5772357723577236                ###
###                                              ###
###  Training with units: 480 epochs: 9          ###
###  f_score: 0.623  ->  movie_units7            ###
###                                              ###
###  Training with units: 768 epochs: 6          ###
###  f_score:  0.6251036312386006                ###
####################################################


####################################################
###                 WW1_PLANES                   ###
###  Training with units: 416 epochs: 11         ###
###  f_score:  0.7499999999999999                ###
###  ww1_planes_units1                           ###
###                                              ###
###  Training with units: 480 epochs: 13         ###
###  f_score:  0.9475806451612903                ###
###  ww1_planes_units4                           ###
####################################################


####################################################
###                    FOOD                      ###
###  Training with units: 288 epochs: 6          ###
###  f_score:  0.695736434108527                 ###
###  food_units1                                 ###
###                                              ###
###  Training with units: 224 epochs: 8          ###
###  f_score:  0.7147876077930374                ###
###  food_epochs2                                ###
####################################################


main()
