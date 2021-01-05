#!/usr/bin/env python
from afinn import Afinn
import sys
import json

afinn = Afinn()
for line in sys.stdin:
    obj  = json.loads(line)
    score = afinn.score(obj["text"])
    obj["afinn_score"] = score
    print(json.dumps(obj,ensure_ascii=False))