# app/scheduler.py

import time
import schedule
from datetime import datetime
from retriever import Retriever
from publisher import Publisher


class Scheduler:
    def __init__(self, batch_size=100, interval_minutes=1):
        self.retriever = Retriever()
        self.publisher = Publisher()
        self.batch_size = batch_size
        self.interval_minutes = interval_minutes

    def job(self):
        print(f"[{datetime.now()}] Running scheduled job...")

        # Fetch a batch of docs from MongoDB
        docs = self.retriever.fetch_batch(limit=self.batch_size)

        # Route to the right Kafka topic
        for doc in docs:
            topic = (
                "raw_tweets_antisemitic"
                if doc.get("antisemitic") in [1, True]
                else "raw_tweets_not_antisemitic"
            )
            self.publisher.publish(topic, doc)

        print(f"Published {len(docs)} messages to Kafka.")

    def run(self):
        # Schedule the job
        schedule.every(self.interval_minutes).minutes.do(self.job)

        print("Scheduler started. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    # from schedule_publishing import Scheduler

    Scheduler().run()
