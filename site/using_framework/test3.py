from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm, BiLstm2
from extraction.model.train import ModelTrainer

def main():
   #loader  = DataHandler("extraction/datasets/planes/ww2_planes.csv")
   #dataset = loader.get_dataset()
   #print(len(loader.getSentences()))
   #training_model = BiLstm("ww2-planes1", "ww2-planes", dataset, (0,0), 512,  0.1, 0.1, 25, 5, 200)
   #trainer = ModelTrainer()
   #trainer.train(training_model, dataset)

   loader = DataHandler("extraction/datasets/MITMovie_dataset.csv")
   dataset = loader.get_dataset()
   training_model = BiLstm("movie")

   plane_model = ExtractionModel("ww1-planes", "ww1-planes2")
   sent = "unit: NO. 55 SQDN bl: 226.0 dept: DAY to PIRMASENS dt: 1917-10-29 desig: AIRCO DH4 DAY BOMBER dummy"
   sent2 = "unit: no. 55 sqdn payload: 224.0kg day to metz-sablon railway siding & station"
   l = plane_model.extract(sent2)
   #l = plane_model.extract
   print(l)

   movie_mode = ExtractionModel("movie", "movie3")
   sent3 = "Drive is a 2011 movie starring Ryan Gosling as an unnamed Hollywood stunt driver who finds himself involved in a large crime syndicate"
   print(sent3)

main()
