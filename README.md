# NLP4NM
A framework for training, testing, and using Named Entity Extraction models
## Folder structure
* `framework\` - NLP4NM framework
  * `datasets\` - NER datasets
  * `model\` - model training/usage code
    * `models` - Loadable trained models*
  * `util\` - Utility functions
* `site\` - Example demo

\* each dataset has its own folder with many trained models in it
## Dependencies
Anaconda pythons default distribution will have all of this. Using a conda environment
### Framework
* Tensorflow 2.0 + Keras (CPU)
* scikitlearn .22
* NLTK 3.4.5
* seqeval

### Demo website
* Flask
* Sqlite3

## Usage  

### Running the demo website
```
cd site
python index.pg
```

### Using the framework
#### Training a model
```python
from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer

loader  = DataHandler("extraction/datasets/planes/ww2_planes.csv")
dataset = loader.get_dataset()
print(len(loader.getSentences()))
training_model = BiLstm("ww2-planes1", "ww2-planes", dataset, (0,0), 512,  0.1, 0.1, 25, 5, 200)
trainer = ModelTrainer()
trainer.train(training_model, dataset)
````

#### Optimizing a model
```python
from extraction.model.extractmodel import ExtractionModel
from extraction.model.dataset import DataHandler
from extraction.model.model import Model, BiLstm
from extraction.model.train import ModelTrainer
from extraction.model.crossvalidation import CrossValidator

loader  = DataHandler('../nlp-model/dataset/MITMovie_dataset.csv')
dataset = loader.get_dataset()

training_model = BiLstm("movie4", "movie", dataset, (0,0), 480, 0.1, 0.1, 100, 32, 9)
trainer = ModelTrainer()
trainer.train(training_model, dataset)
best_model = CrossValidator(dataset, 'movie', ['movie1', 'movie2', 'movie3', 'movie4']).compare()
print(best_model, " was determined to be the best model")

main()
```
#### Using a model
