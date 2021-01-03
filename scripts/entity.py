import sys
import spacy
import json

nlp = spacy.load('en_core_web_sm')

for line in sys.stdin:
	obj  = json.loads(line)	 
	doc = nlp(obj["tweet"])
	ents = []
	for entity in doc.ents:	
		ents.append({"label":entity.label_ ,"entity": entity.text })
	obj["entities"] = ents 
	print(json.dumps(obj))
