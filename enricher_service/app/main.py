class EnricherService:
    def __init__(self, topics, max_messages=50):
        from common.consumer.app.kafka_consumer import read_news
        self.topics = topics
        self.max_messages = max_messages
        self.messages = []

    def run(self):
        from cleaning.app.enricher import CleaningEnricher
        for topic in self.topics:
            self.messages += read_news(topic, self.max_messages)
        enricher = CleaningEnricher()
        enricher.df = enricher.df  # assign consumed data if needed
        enricher.emotion_text()
        enricher.find_weapon_name()
        self.publish_messages(enricher.df)

    def publish_messages(self, df):
        from common.publisher import Publisher
        publisher = Publisher()
        for _, row in df.iterrows():
            msg = {
                "original_text": row["text"],  # keep original
                "clean_text": row["clean_text"],  # cleaned text
                "sentiment": row["type_text"],  # from emotion_text()
                "weapons": row["weapons_detected"]  # from find_weapon_name()
            }
            topic = (
                "enriched_preprocessed_tweets_antisemitic"
                if row.get("antisemitic") == 1
                else "enriched_preprocessed_tweets_not_antisemitic"
            )
            publisher.publish(topic, msg)
