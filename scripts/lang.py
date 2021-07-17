#!/usr/bin/env python3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import json
import fasttext

model = fasttext.load_model('models/lid.176.ftz')
for line in sys.stdin:
    obj  = json.loads(line)
    prediction = model.predict(obj["text"].replace("\n",""),k=1)
    if len(prediction) > 1:
            if prediction[1][0] > 0.80:
                obj["lang"] = prediction[0][0].split("__")[-1]
            else:
                obj["lang"] = "UNKNOWN"
    print(json.dumps(obj,ensure_ascii=False)) 
