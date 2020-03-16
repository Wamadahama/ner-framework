import json
import nltk
from nltk import * 
from nltk.tag.stanford import StanfordPOSTagger
from os.path import expanduser

tags = [
    "Instruction"
    "Instrument",
    "Ingredient",
    "Other"
]

manual_fixes = [
    ['PREHEAT', 'VB'],
    ['PRESS', 'VB'],
    ['MIX', 'VB'],
    ['COOK', 'VB'],
    ['PAN', 'NN'],
    ['PLACE', 'VB'],
    ['(', '('],
    [')', ')'],
    ['BAKE', 'VB'],
    ['BLACK', 'NN'],
    ['BEATEN', 'NN']
]

set = [
    ["B-INSTRUMENT", "I-INSTRUMENT"],
    ["B-MEASUREMENT", "I-INSTRUMENT"]
]



def get_item(dataset,keys,i):
    return dataset[keys[i]]['instructions']

def apply_fixes(sentence):
    return_sentence = []
    for word in sentence:
        skip = False
        for pair in manual_fixes:
            if word[0].upper() == pair[0]:
                return_sentence.append((word[0], pair[1]))
                skip = True
                break
        if skip == False:
            return_sentence.append(word)
    return return_sentence

# "Chunk:
# {<JJ><NN>+} -> May correspond to an instrument ie- large pan, deep bowl 
#{<VB><PRP>?<IN>?<RB>?<NN>*} -> instructions involve verbs and prepositions 
#{<VB><PRP>?<IN>?<NN>?<RB>?<VB>?<NN>+}
#Instruction:{(IN)?(DT)?(<VB>|<VBG>|<IN>)(DT)?(<NN>?<IN>?(<CD>|<NN>|<TO>)+(<NN>|<NNS>)?)+}

def chunk(tagged_sentence):
    #grammar = r"""Instrument:{<JJ><NN>+}
    #              Instruction:{(<VB>|<VBG>)(<IN>|<RB>|<PDT>)?<DT>?(<NN>|<NNP>|<NNS>)(<NN>?<IN>?)+}"""

    grammar = r"""Instrument:{<JJ><NN>+}
                  Measurement: {<CD>(<NN>|<NNS>)+}
                  """
    parser = nltk.RegexpParser(grammar)
    chnk = parser.parse(tagged_sentence)
    return chnk

def tree2conlltags(t):
    """
    Return a list of 3-tuples containing ``(word, tag, IOB-tag)``.
    Convert a tree to the CoNLL IOB tag format.

    :param t: The tree to be converted.
    :type t: Tree
    :rtype: list(tuple)
    """

    tags = []
    for child in t:
        try:
            category = child.label()
            prefix = "B-"
            for contents in child:
                if isinstance(contents, Tree):
                    raise ValueError("Tree is too deeply nested to be printed in CoNLL format")
                tags.append((contents[0], contents[1], prefix+category))
                prefix = "I-"
        except AttributeError:
            tags.append((child[0], child[1], "O"))
    return tags 


def main():
    home = expanduser("~")
    with open('recipes_raw_nosource_ar.json', 'r') as f:
        dataset = json.loads(f.read())

    keys = list(dataset.keys())

    # Use stanford pos tagger
    tagger = StanfordPOSTagger(model_filename=home + "/nlp4nm/packages/stanford-postagger/models/wsj-0-18-bidirectional-distsim.tagger",
                       path_to_jar=home+"/nlp4nm/packages/stanford-postagger/stanford-postagger.jar")

    n=1024

    for i in range(1, n):
        item = get_item(dataset, keys,i)
        tokenized_text = word_tokenize(item)
        #pos_tags = nltk.pos_tag(tokenized_text)
        pos_tags = apply_fixes(tagger.tag(tokenized_text))
        #print(pos_tags)
        chunked_sent = chunk(pos_tags)
        #print(type(chunked_sent))
        connl_tags = tree2conlltags(chunked_sent)
        for tag in connl_tags:
            print("{},{}".format(tag[0], tag[2]))
        #for subtree in chunked_sent.subtrees(filter=lambda t: t.label() == 'Instrument'):
        #    print(subtree)
        #print("------ Example {} ------".format(i))
        #print(chunked_sent)
        #print("-------------------------")

main()
