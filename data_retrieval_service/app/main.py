from fastapi import FastAPI
from db import MongoDBClient

app = FastAPI(title="Data Retrieval Service")

mongo_client = MongoDBClient()

@app.get("/antisemitic_tweets")
def get_antisemitic_tweets():
    """
    Return all antisemitic tweets from MongoDB.
    """
    collection = mongo_client.get_collection("tweets_antisemitic")
    tweets = list(collection.find({}, {"_id": 0}))  # hide MongoDB internal _id
    return {"count": len(tweets), "tweets": tweets}

@app.get("/not_antisemitic_tweets")
def get_not_antisemitic_tweets():
    """
    Return all non-antisemitic tweets from MongoDB.
    """
    collection = mongo_client.get_collection("tweets_not_antisemitic")
    tweets = list(collection.find({}, {"_id": 0}))
    return {"count": len(tweets), "tweets": tweets}
