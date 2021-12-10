#!/usr/bin/env python3
 
import sys
from kafka import KafkaProducer
import argparse


parser = argparse.ArgumentParser(
    description='Subscribe to kafka topic, syntax: ./kafka2json.py -topic mytopic -endpoint 10.232.3.2.3:1234 -groupId mygroup')
parser.add_argument('-topic', required=True, type=str, nargs=1,
                    help='Kafka topic to which we need to subscribe to.')
parser.add_argument('-endpoint', required=True, type=str, nargs=1,
                    help='Kafka server endpoint and port.')

args, unknown = parser.parse_known_args()


producer = KafkaProducer(bootstrap_servers=args.endpoint[0])
for line in sys.stdin:
    producer.send(args.topic[0], str.encode(line.strip()))
    producer.flush()

 