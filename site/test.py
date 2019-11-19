from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler 
from extraction.model.model import Model, BiLstm


def main():
    # Test Model training:

#from dataset import DataHandler
    #d_set1 = DataHandler('../../../nlp-model/dataset/MITMovie_dataset.csv')
    #sentences = d_set1.getSentences()
    #X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = d_set1.get_train_test(sentences=sentences, test_size=0.1, max_len=30)

    loader  = DataHandler("extraction/datasets/re3d_dataset.txt")
    dataset = loader.get_dataset()
    training_model = BiLstm("re3d1", "re3d", dataset, (0,0), 512, 0.1, 0.1, 70, 30, 100).get_model()
    #model = ExtractionModel("movie")
#    model.extract("Ryan Gosling in the movie Drive where the driver finds himself entagled in a crime syndicate")
    #dt = model.extract('Blade Runner is a 1982 science fiction film directed by Ridley Scott This film is set in a dystopian future Lost Angeles of 2019') 
    #print(dt)
#    model.extract("i m thinking of a 1988 action film in which bruce willis a nypd officer fights off terrorists")
#in which synthetic ehumans known as replicants e bio-engineered by the powerful Tyrell Corporation to work on off-world Colonies. Written by hampton Francher and David Peoples')

main()
