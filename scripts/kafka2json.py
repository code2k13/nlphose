#!/usr/bin/env python3
 
import json
from kafka import KafkaConsumer
import argparse


parser = argparse.ArgumentParser(
    description='Subscribe to kafka topic, syntax: ./kafka2json.py -topic mytopic -endpoint 10.232.3.2.3:1234 -groupId mygroup')
parser.add_argument('-topic', required=True, type=str, nargs=1,
                    help='Kafka topic to which we need to subscribe to.')
parser.add_argument('-endpoint', required=True, type=str, nargs=1,
                    help='Kafka server endpoint and port.')
parser.add_argument('-groupId', required=True, type=str, nargs=1,
                    help='Kafka Group Id.')

args, unknown = parser.parse_known_args()


consumer = KafkaConsumer(args.topic[0], group_id=args.groupId[0],bootstrap_servers=args.endpoint[0])
for msg in consumer:
    print(json.dumps(str(msg.value),ensure_ascii=False))

 

 