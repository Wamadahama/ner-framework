from dataset import DataHandler
d_set1 = DataHandler('../../../nlp-model/dataset/MITMovie_dataset.csv')
sentences = d_set1.getSentences()
X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = d_set1.get_train_test(sentences=sentences, test_size=0.1, max_len=30)
