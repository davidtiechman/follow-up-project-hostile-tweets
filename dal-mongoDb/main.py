
from fastapi import FastAPI
from kafka import KafkaConsumer
from pymongo import MongoClient
import threading
from datetime import datetime

app = FastAPI(title="Subscriber - Interesting")

# MongoDB Setup
client = MongoClient("mongodb://mongo:27017/")  # container name 'mongo'
db = client["newsgroups_db"]
collection = db["interesting"]

# Kafka Consumer
def consume_messages():
    consumer = KafkaConsumer(
        "interesting",
        bootstrap_servers="kafka:9092",
        auto_offset_reset="earliest",
        group_id="subscriber_interesting_group",
        value_deserializer=lambda v: v.decode("utf-8")  # <- decode raw string
    )

    for msg in consumer:
        # Insert as document into MongoDB
        collection.insert_one({
            "message": msg,
            "timestamp": str(datetime.utcnow())
        })

# Run consumer in background thread
threading.Thread(target=consume_messages, daemon=True).start()

@app.get("/messages")
def get_messages():
    return list(collection.find({}, {"_id": 0}))