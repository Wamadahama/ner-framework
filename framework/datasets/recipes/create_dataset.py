import json
import nltk
from nltk import * 

tags = [
    "Ingredient",
    "Instruction"
    "Cookware",
    "Other"
]

with open('recipes_raw_nosource_ar.json', 'r') as f:
    dataset = json.loads(f.read())

keys = list(dataset.keys())
test_item = dataset[keys[0]]['instructions']
print(test_item)

tokenized_text = word_tokenize(test_item)
pos_tags = nltk.pos_tag(tokenized_text)

print(pos_tags)
