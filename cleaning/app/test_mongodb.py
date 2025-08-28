from kafka import KafkaProducer
import json
from consumer.app.kafka_configurations import BOOTSTRAP_SERVERS
from publisher.app.load_data import load_data
def publishing_to_kafka(topic):
    TOPIC_NAME = topic
    GROUP_ID = topic
    producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    message = load_data(topic)
    for message in message:
        producer.send(TOPIC_NAME, message)
    producer.flush()
    print("Message sent!")
# import pymongo
# import pandas as pd
# def load_data():
#     myclient = pymongo.MongoClient(host="mongodb+srv://IRGC_NEW:iran135@cluster0.6ycjkak.mongodb.net/")
#     mydb = myclient["IranMalDB"]
#     mycol = mydb["tweets"]
#     mongo = mycol.find().limit(5)
#     return mongo
#
# def convert_by_df(mongo):
#     mongo = list(mongo)
#     df = pd.DataFrame(mongo)
#     return df
# # mongo = load_data()
# # df = convert_by_df(mongo)
# # print(df.columns)
import time
import schedule
from datetime import datetime
# from retriever import Retriever
# from publisher import Publisher
import retriever
import publisher

class Scheduler:
    def __init__(self, batch_size=100, interval_minutes=1):
        self.retriever = Retriever()
        self.publisher = Publisher()
        self.batch_size = batch_size
        self.interval_minutes = interval_minutes

    def job(self):
        print(f"[{datetime.now()}] Running scheduled job")
        # Fetch a batch of docs from MongoDB
        docs = self.retriever.fetch_batch(limit=self.batch_size)
        # Route to the right Kafka topic
        topic = ''
        for doc in docs:
            if doc['Antisemitic']:
                topic = "raw_tweets_antisemitic"
            else:
                topic = "raw_tweets_not_antisemitic"
            self.publisher.publish(topic, doc)

        print(f"Published {len(docs)} messages to Kafka.")
        # print(docs)

    def run(self):
        # Schedule the job
        schedule.every(self.interval_minutes).minutes.do(self.job)

        print("Scheduler started. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(1)
a = Scheduler()
a.job()