from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm, BiLstm2
from extraction.model.train import ModelTrainer

def main():
   loader  = DataHandler("extraction/datasets/planes/ww1_planes.csv")
   dataset = loader.get_dataset()
   print(len(loader.getSentences()))
   training_model = BiLstm("ww1-planes1", "ww1-planes", dataset, (0,0), 128,  0.1, 0.1, 25, 36, 5)
   trainer = ModelTrainer()
   trainer.train(training_model, dataset)


   plane_model = ExtractionModel("ww1-planes", "ww1-planes1")
   sent = "unit: NO. 55 SQDN bl: 226.0 dept: DAY to PIRMASENS dt: 1917-10-29 desig: AIRCO DH4 DAY BOMBER dummy"
   l = plane_model.extract(sent)
   print(l)


main()
