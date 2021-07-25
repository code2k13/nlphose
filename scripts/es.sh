#!/bin/bash
while IFS='$\n' read -r line; do
        curl -s -o /dev/null  -H "Content-Type: application/json" -X POST -d "$line" "localhost:9200/nlphose/data"
done