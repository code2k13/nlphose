#!/usr/bin/env python3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import argparse
from transformers import pipeline
import sys
import json

parser = argparse.ArgumentParser(
    description='Run transformer model on incoming json')
parser.add_argument('--pipeline', required=True, type=str, nargs='+',
                    choices=['sentiment-analysis',
                             'question-answering', 'zero-shot-classification'],
                    help='Name of pipeline, currently supported : sentiment-analysis,question-answering or zero-shot-classification')
parser.add_argument('--param',   type=str, nargs=1)
parser.add_argument('--device', required=False, type=int, nargs=1, default=-1)


args = parser.parse_args()

if args.pipeline[0] in ['question-answering', 'zero-shot-classification']:
    if args.param == None:
        raise Exception(
            "--param is required for question-answering and zero-shot-classification task!  ")


device = args.device
if isinstance(device, list):
    device = args.device[0]

pipeline = pipeline(args.pipeline[0], device=device)

for line in sys.stdin:
    obj = json.loads(line)
    attribute_name = 'xfrmr-'+args.pipeline[0]
    attribute_name = attribute_name.replace("-","_")
    if attribute_name not in obj:
        obj[attribute_name] = None
    if args.pipeline[0] == 'sentiment-analysis':
        obj[attribute_name] = pipeline(obj["text"])
    elif args.pipeline[0] == 'question-answering':
        obj[attribute_name] = pipeline(
            context=obj["text"], question=args.param[0])
    elif args.pipeline[0] == 'zero-shot-classification':
        obj[attribute_name] = pipeline(
            obj["text"], candidate_labels=args.param[0].split("#"))
        del obj[attribute_name]["sequence"]

    print(json.dumps(obj, ensure_ascii=False))
