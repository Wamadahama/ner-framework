from framework.model.extractmodel import ExtractionModel
from framework.model.dataset import DataHandler
from framework.model.model import Model, BiLstm
from framework.model.train import ModelTrainer

def main():
    loader  = DataHandler('./framework/datasets/MITMovie_dataset.csv')
    dataset = loader.get_dataset()
    training_model = BiLstm("movie4", "movie", dataset, (0,0), 2, 0.1, 0.1, 100, 32, 1)
    trainer = ModelTrainer()
    trainer.train(training_model, dataset)

    trained_model = ExtractionModel("movie", "movie4") 
    print(trained_model.extract("Drive is a 2011 movie starring Ryan Gosling as an unamed Hollywood stunt driver who finds himself involved in a large crime syndicate"))

main()
