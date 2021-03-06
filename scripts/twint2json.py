#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    s = line.split(" ")
    obj = {}
    obj['id'] = s[0]
    obj['date'] = s[1] + " " + s[2] + " " + s[3]
    obj['user'] = s[4]
    obj['text'] = " ".join(s[5:])
    print(json.dumps(obj,ensure_ascii=False))