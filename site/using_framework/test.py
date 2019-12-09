from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer
#from extraction.model.crossvalidation import CrossValidator

def main():
#   loader  = DataHandler("extraction/datasets/re3d_dataset.txt")
#   dataset = loader.get_dataset()
#   training_model = BiLstm("re3d1", "re3d", dataset, (0,0), 512, 0.1, 0.1, 70, 200, 1)
#   trainer = ModelTrainer()
#   trainer.train(training_model, dataset)

   movie_model = ExtractionModel("movie", "movie3")
   dt = movie_model.extract("Ryan Gosling in the movie Drive where the driver finds himself entagled in a crime syndicate")
   print(dt)













'''
#    print(dt)
    #dt = model.extract('Blade Runner is a 1982 science fiction film directed by Ridley Scott This film is set in a dystopian future Lost Angeles of 2019')
    #print(dt)
#    model.extract("i m thinking of a 1988 action film in which bruce willis a nypd officer fights off terrorists")
#in which synthetic ehumans known as replicants e bio-engineered by the powerful Tyrell Corporation to work on off-world Colonies. Written by hampton Francher and David Peoples')



    #loader  = DataHandler('../nlp-model/dataset/MITMovie_dataset.csv')
    #dataset = loader.get_dataset()
    
# O	what
# O	is
# O	the
# B-Genre	italian
# I-Genre	language
# O	film
# O	by
# B-Director	frederico
# I-Director	fellini
# O	that
# B-Plot	focuses
# I-Plot	on
# I-Plot	a
# I-Plot	photographer
# I-Plot	and
# I-Plot	the
# I-Plot	decadence
# I-Plot	of
# I-Plot	modern
# I-Plot	life

    i = model.extract("what is the italian language film by frederico fellini that focuses on a photographer and the decadence of modern life")
    print(i)
    # name, group, dataset, input_shape, lstm_units, dropout, recurrent_dropout, embedding_output_dimensions, batch_size, epochs
    training_model = BiLstm("movie1", "movie", dataset, (0,0), 512, 0.1, 0.1, 50, 32, 2)
    trainer = ModelTrainer()
    trainer.train(training_model, dataset)

    training_model2 = BiLstm("movie2", "movie", dataset, (0,0), 256, 0.1, 0.1, 100, 64, 3)
    trainer = ModelTrainer()
    trainer.train(training_model2, dataset)

                              #<dataset,  group     model1    model2>
    best_model = CrossValidator(dataset, 'movie', ['movie1', 'movie2']).compare()
    print(best_model, " was determined to be the best model")
    # best_model = crossvaldation(model1, model2) #where model1 and model2 are instances of 'model class'
'''
main()
