from framework.model.extractmodel import ExtractionModel
from framework.model.dataset import DataHandler
from framework.model.model import Model, BiLstm, BiLstm2
from framework.model.train import ModelTrainer

def main():
   movie_model = ExtractionModel("movie", "movie4")
   sent3 = "Drive is a 2011 movie starring Ryan Gosling as an unnamed Hollywood stunt driver who finds himself involved in a large crime syndicate"
   dt = movie_model.extract(sent3)
   print(dt)

main()
