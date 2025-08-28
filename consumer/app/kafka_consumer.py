from kafka import KafkaConsumer
import json
from consumer.app.kafka_configurations import (BOOTSTRAP_SERVERS)


def read_news(topic: str,max_massages: int):
    TOPIC_NAME = topic
    GROUP_ID = None
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        consumer_timeout_ms=5000)
    arr = []
    count = 0
    for message in consumer:
        arr.append({'message': message.value, 'timestamp': message.timestamp,'topic': message.topic})
        count += 1
        if count >= max_massages:
            break
    if len(arr) > 0:
        print('len message:',len(arr) )
        # insert_to_mongo(TOPIC_NAME,arr)
    else:
        print('no new messages')
    return arr

# print(read_news('raw_tweets_antisemitic',10))
