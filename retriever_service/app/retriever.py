# app/retriever.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Make sure env vars are loaded

class Retriever:
    def __init__(self, collection_name="tweets"):
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB")
        if not uri or not db_name:
            raise ValueError("Missing MongoDB URI or DB name in .env")

        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_all(self):
        return list(self.collection.find({}))

    def fetch_batch(self, limit=100):
        """
        Fetch the oldest `limit` documents sorted by timestamp
        """
        return list(
            self.collection.find({}, sort=[("timestamp", 1)], limit=limit)
        )


if __name__ == "__main__":
    R = Retriever()
    print(R.fetch_batch(10))  # Fetch 10 oldest docs
