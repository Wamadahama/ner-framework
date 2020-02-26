from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm, BiLstmCRF, BiLstm_2layers, BiLstm_3layers
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator
from extraction.model.optimize import Optimizer
from threading import Thread
import time

def main():
    loader = DataHandler("extraction/datasets/MITMovie_dataset.csv")
    dataset = loader.get_dataset()

    num_units = 216
    num_epochs = 2
    num_layers = 4
    unit_step = 16
    initial_model = BiLstm_3layers("movie001", "movie", dataset, (0,0), num_units, num_layers, 0.1, 0.1, 70, 64, num_epochs)

    trainer = ModelTrainer()
    initial_trained_model = trainer.train(initial_model, dataset)
    iter = 1
    while True:
        units_name = "movie_units"+str(iter)
        training_model = BiLstm_3layers(units_name, "movie", dataset, (0,0), num_units+unit_step, num_layers, 0.1, 0.1, 70, 64, num_epochs)
        trainer = ModelTrainer()
        trained_model1 = trainer.train(training_model1, dataset)
        
        epochs_name = "movie_epochs"+str(iter)
        trained_model = BiLstm_3layers(epochs_name, "movie", dataset, (0,0), num_units, num_layers, 0.1, 0.1, 70, 64, num_epochs+1)
        trainer = ModelTrainer()
        trained_model2 = trainer.train(training_model2, dataset)
         
        if iter == 1:
            best_model = CrossValidator(dataset, "movie", ["movie001", units_name, epochs_name]).compare()
        else:
            best_model = CrossValidator(dataset, "movie", [units_name, epochs_name]).compare()
            
        if best_model == "movie001":
            print("Initial model was the best model")
            break
        elif best_model == units_name:
            num_units += 256
            print("No. of units now changed to: ", num_units)
        else:
            num_epochs += 1
            print("No. of epochs now changed to: ", num_epochs)
            
main()
