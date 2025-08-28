from app.persister import PersisterService

if __name__ == "__main__":
    # Topics to consume
    topics = [
        "enriched_preprocessed_tweets_antisemitic",
        "enriched_preprocessed_tweets_not_antisemitic"
    ]
    service = PersisterService(topics, max_messages=50)
    service.run()
