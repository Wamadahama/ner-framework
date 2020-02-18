from framework.model.extractmodel import ExtractionModel
from framework.model.dataset import DataHandler
from framework.model.model import Model, BiLstm
from framework.model.train import ModelTrainer
#from framework.model.crossvalidation import CrossValidator

def main():
    loader  = DataHandler('./framework/datasets/MITMovie_dataset.csv')
    dataset = loader.get_dataset()
    training_model = BiLstm("movie4", "movie", dataset, (0,0), 2, 0.1, 0.1, 100, 32, 1)
    trainer = ModelTrainer()
    trainer.train(training_model, dataset)#    best_model = CrossValidator(dataset, 'movie', ['movie1', 'movie2', 'movie3', 'movie4']).compare()
#    print(best_model, " was determined to be the best model")

main()
