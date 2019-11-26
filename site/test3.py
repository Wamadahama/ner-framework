from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm, BiLstm2
from extraction.model.train import ModelTrainer

def main():
#   loader  = DataHandler("extraction/datasets/planes/ww1_planes.csv")
#   dataset = loader.get_dataset()
#   training_model = BiLstm2("ww1-planes1", "ww1-planes", dataset, (0,0),50, 128, 0.1, 0.1, 25, 36, 5)
#   trainer = ModelTrainer()
#   trainer.train(training_model, dataset)

   plane_model = ExtractionModel("ww1-planes", "ww1-planes1")
   l = plane_model.extract("unit: NO.55 SQDN")
   print(l)


main()
