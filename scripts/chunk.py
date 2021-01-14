#!/usr/bin/env python3
import sys
import json
import nltk

nltk.download('averaged_perceptron_tagger',  quiet=True)
nltk.download('punkt', quiet=True)
 
if len(sys.argv) != 3:
    print("invalid agruments for chunking. Usage : ./chunk.py pattern_name pattern")
    exit()
 

for line in sys.stdin:
    obj  = json.loads(line)
    if 'chunks' not in obj:
        obj['chunks'] = []
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(obj['text']))
    grammar = "NP: " + sys.argv[2]
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(tagged_sentence)
    output = []
    trees = [subtree for subtree in result if type(subtree) == nltk.Tree and subtree.label() == "NP"]
    for tree in trees:
        phrase = []
        for leaf in tree:
            phrase.append(leaf[0])
        obj['chunks'].append([sys.argv[1], ' '.join(phrase)])
    print(json.dumps(obj,ensure_ascii=False))
