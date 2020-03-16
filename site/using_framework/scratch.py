from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator

def main():
    loader  = DataHandler('../nlp-model/dataset/MITMovie_dataset.csv')
    dataset = loader.get_dataset()

    training_model = BiLstm("movie4", "movie", dataset, (0,0), 480, 0.1, 0.1, 100, 32, 9)
    trainer = ModelTrainer()
    trainer.train(training_model, dataset)
    best_model = CrossValidator(dataset, 'movie', ['movie1', 'movie2', 'movie3', 'movie4']).compare()
    print(best_model, " was determined to be the best model")

main()
