from tensorflow.keras import Input
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Flatten, Lambda

class BaseModel:
    def __init__(self, name, group, dataset, input_shape):
        self.name = name # name of the model
        self.group = group
        self.dataset = dataset  # Dataset() object
        self.input_shape = input_shape # Input shape

class BiLstm(BaseModel):
    """Bi-Lstm model information"""
    def __init__(self, name, group, dataset, input_shape, lstm_units, dropout, recurrent_dropout, embedding_output_dimensions, batch_size, epochs):
        """ All information required for training """
        super().__init__(name, group, dataset, input_shape)
        self.lstm_units = lstm_units # TODO: write a method for determining units by default
        self.dropout = dropout # Dropout layer
        self.recurrent_dropout = recurrent_dropout # LSTM recurrent dropout
        self.embedding_output_dimensions = embedding_output_dimensions # First embedding layer
        #self.output_dimensions = output_dimensions # might be a part of Dataset
        # Training hyperparameters
        self.batch_size = batch_size
        self.epochs = epochs

    def get_model(self):
        try:
            input = Input(shape=(self.dataset.max_len, ))
            embedding = Embedding(input_dim=self.dataset.n_words, output_dim = self.embedding_output_dimensions, input_length = self.dataset.max_len)(input)
            lstm_layer = Bidirectional(LSTM(units=self.lstm_units, return_sequences=True,
                                            recurrent_dropout=self.recurrent_dropout,
                                            dropout=self.dropout))(embedding)
            output_layer = TimeDistributed(Dense(self.dataset.n_tags, activation='softmax'))(lstm_layer)
            model = Model(input, output_layer)
            return model

        except Exception as e:
            print("Unable to compile model") # more descriptive errors
            print(e)
