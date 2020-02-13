import json
import os


GLOBAL_VOCAB_FILE = 'framework/vocab/GlobalVocab.json'

def generate_vocab_from_list():
    """
    Takes a \r\n separated wordlist and generates a vocabulary in the desired json format
    [
    { "word": "moviedirected", "index": 0 },
    { "word": "moviedirected", "index": 0 },
    ...
    { "word": "moviedirected", "index": 0 },
    ]
    """
    with open("wordlist.txt", 'r', encoding='iso8859-1') as f:
        text = f.read()
    words = text.split("\n")
    wl = [{ "word": word, "index": i} for i,word in enumerate(words, 0)]

    with open(GLOBAL_VOCAB_FILE, "w") as f:
        f.write(json.dumps(lst))

def load_global_vocabulary(filename=""):
    if filename == "":
        with open(GLOBAL_VOCAB_FILE, 'r') as f:
            vocab = json.load(f)
    else:
        with open(filename, 'r') as f:
            vocab = json.load(f)
    return vocab

def merge_vocabs(vocab1, vocab2):
    """
    Takes vocab1,vocab2 -> List[DictItems]
    in the form 
    [
    { "word": "moviedirected", "index": 0 },
    { "word": "moviedirected", "index": 0 },
    ...
    { "word": "moviedirected", "index": 0 },
    ]
    """
    index_start = len(vocab1)
    for item in vocab2:
        dict_item = {}
        #print(word, index)
        dict_item["word"] = item["word"]
        dict_item["index"] = item["index"]
        index_start += 1 
        vocab1.append(dict_item)
    return vocab1
