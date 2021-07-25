#!/usr/bin/env python3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import spacy
import json
from geocode.geocode import Geocode

gc = Geocode()
gc.load() 
nlp = spacy.load('en_core_web_sm')

for line in sys.stdin:
	obj  = json.loads(line)	 
	doc = nlp(obj["text"])
	ents = []
	for entity in doc.ents:	
		entity_obj = {"label":entity.label_ ,"entity": entity.text }
		if entity.label_ == "GPE":
			cords = gc.decode(entity.text)
			if len(cords) > 0:
				entity_obj['cords'] = {"lat":cords[0]["latitude"],"lon":cords[0]["longitude"]}	 	
		ents.append(entity_obj)
	obj["entities"] = ents 
	print(json.dumps(obj,ensure_ascii=False))
