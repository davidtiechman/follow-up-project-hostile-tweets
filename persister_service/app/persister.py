from common.consumer.app.kafka_consumer import read_news
from app.mongodb_client import MongoDBClient
import json

class PersisterService:
    def __init__(self, topics, max_messages=100):
        self.topics = topics
        self.max_messages = max_messages
        self.messages = []
        self.mongo_client = MongoDBClient()
        # Define collections
        self.antisemitic_col = self.mongo_client.get_collection("tweets_antisemitic")
        self.not_antisemitic_col = self.mongo_client.get_collection("tweets_not_antisemitic")

    def run(self):
        # Consume messages from all topics using the common consumer
        for topic in self.topics:
            self.messages += read_news(topic, self.max_messages)
        # Insert into MongoDB
        self.persist_messages()

    def persist_messages(self):
        for msg in self.messages:
            data = json.loads(msg['message'])  # assumes Kafka message has 'message' field
            if data.get("antisemitic") == 1:
                self.antisemitic_col.insert_one(data)
            else:
                self.not_antisemitic_col.insert_one(data)
        print(f"Inserted {len(self.messages)} messages into MongoDB")
