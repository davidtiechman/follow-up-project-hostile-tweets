import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # load service-specific env

class MongoDBClient:
    """
    Connect to MongoDB using env variables and provide access to collections.
    """
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
        db_name = os.getenv("MONGO_DB", "twitter")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]
