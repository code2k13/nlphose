#!/usr/bin/env python3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import argparse
import json
import sys
import uuid

parser = argparse.ArgumentParser(
    description='convert text file/s to JSON documents, syntax: ./file2json.py -n *.py')
parser.add_argument('-n', required=True, type=int, nargs=1,
                    help='Number of sentences to group together in a single JSON document.')

args, unknown = parser.parse_known_args()

from spacy.lang.en import English
nlp = English()
max_group_lines = int(args.n[0])
max_lines = 128 
nlp.add_pipe('sentencizer')

def read_line(file):
    ctr = 0
    lines = []
    with open(filename) as f:
        while True:
            line  = f.readline()
            if not line:
                break
            line = line.strip()
            lines.append(line)
            ctr = ctr + 1
            if((ctr >= max_group_lines and len(line) > 0 and line[-1]=='.' ) or len(lines) > max_lines) :
                ctr = 0
                retval  = ' '.join(lines) 
                lines = []
                yield retval     
            
        yield ' '.join(lines)  
 
filenames = unknown
lines = []
line = ''

for filename in filenames:
    for doc in read_line(filename):
        d = nlp(doc)
        document = {}
        document['file_name']  = filename
        document['id']  = str(uuid.uuid1())
        document['text'] = ' '.join([str(s) for s in d.sents])
        print(json.dumps(document, ensure_ascii=False))
         
