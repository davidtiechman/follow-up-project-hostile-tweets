import os
import json
from kafka import KafkaProducer
from dotenv import load_dotenv

from consumer.app.kafka_configurations import BOOTSTRAP_SERVERS

load_dotenv()  # Load env vars

class Publisher:
    def __init__(self):
        # Kafka broker(s)
        # brokers = os.getenv("KAFKA_BROKERS")
        brokers = BOOTSTRAP_SERVERS
        self.producer = KafkaProducer(
            bootstrap_servers=brokers.split(","),
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8")

        )

    def publish(self, topic: str, message: dict):
        """
        Publish a single message (dict) to the given Kafka topic
        """
        self.producer.send(topic, value=message)
        self.producer.flush()  # Ensure it is sent immediately
        print(f"Published message to {topic}")


