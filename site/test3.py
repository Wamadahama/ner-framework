from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer

def main():
   loader  = DataHandler("extraction/datasets/planes/ww1_planes.csv")
   dataset = loader.get_dataset()
   training_model = BiLstm("ww1-planes", "1", dataset, (0,0), 512, 0.1, 0.1, 70, 36, 200)
   trainer = ModelTrainer()
   trainer.train(training_model, dataset)


main()
