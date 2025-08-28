from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load the .env file in the service's folder
load_dotenv()

class MongoDBClient:
    """
    Connect to MongoDB using environment variables and provide access to collections.
    """

    def __init__(self):
        # Read MongoDB URI and database name from environment variables
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")  # fallback to default
        db_name = os.getenv("MONGO_DB", "twitter")  # fallback to default

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        """
        Return a MongoDB collection object.
        """
        return self.db[collection_name]
