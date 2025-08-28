
import time
import schedule
from datetime import datetime

from retriever_service.app.publisher import Publisher
from retriever_service.app.retriever import Retriever


class Scheduler:
    def __init__(self, batch_size=100, interval_minutes=1):
        self.retriever = Retriever()
        self.publisher = Publisher()
        self.batch_size = batch_size
        self.interval_minutes = interval_minutes

    @staticmethod
    def _is_antisemitic(doc: dict) -> bool:
        """
        Returns True if the document is marked as antisemitic.
        Supports different keys and types: 1/0, True/False, "1"/"0"/"true"/"false".
        """
        # Try several possible keys
        candidates = [
            doc.get("antisemitic"),
            doc.get("Antisemitic"),
            (doc.get("prediction") or {}).get("antisemitic") if isinstance(doc.get("prediction"), dict) else None,
        ]
        v = next((x for x in candidates if x is not None), None)

        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return int(v) == 1
        if isinstance(v, str):
            return v.strip().lower() in {"1", "true", "yes", "y"}
        return False  # Default fallback

    def job(self):
        print(f"[{datetime.now()}] Running scheduled job...")

        # Fetch a batch from MongoDB
        docs = self.retriever.fetch_batch(limit=self.batch_size)

        count_anti = 0
        count_not = 0

        # Route each document to the correct Kafka topic
        for doc in docs:
            if self._is_antisemitic(doc):
                topic = "raw_tweets_antisemitic"
                count_anti += 1
            else:
                topic = "raw_tweets_not_antisemitic"
                count_not += 1

            self.publisher.publish(topic, doc)

        print(f"Published {len(docs)} messages to Kafka. "
              f"(antisemitic={count_anti}, not_antisemitic={count_not})")

    def run(self):
        schedule.every(self.interval_minutes).minutes.do(self.job)
        print("Scheduler started. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    Scheduler().run()

