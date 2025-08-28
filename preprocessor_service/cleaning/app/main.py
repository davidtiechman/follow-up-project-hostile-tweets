
from common.consumer.app.kafka_consumer import read_news
from common.publisher import Publisher
from preprocessor_service.cleaning.app.processor import InitialCleanText


class ProcessorService:
    def __init__(self, topics, max_messages=100):

        self.topics = topics
        self.max_messages = max_messages
        self.messages = []

    def run(self):
        # Consume from all topics
        for topic in self.topics:
            self.messages += read_news(topic, self.max_messages)
        # Process messages
        self.process_messages()

    def process_messages(self):
        # Pass consumed messages into the cleaner
        cleaner = InitialCleanText(self.messages)

        cleaner.remove_punctuation()
        cleaner.remove_spaces()
        cleaner.remove_extra_whitespace()
        cleaner.convert_text_to_lowercase()
        cleaner.division_text()
        cleaner.remove_stopwords()
        cleaner.find_root_of_word()
        cleaner.retrons_to_string()

        # Publish results
        self.publish_messages(cleaner.df)

    def publish_messages(self, df):
        publisher = Publisher()  # create once
        for _, row in df.iterrows():
            msg = {
                "original_text": row["text"],
                "clean_text": row["clean_text"]
            }
            topic = (
                "preprocessed_tweets_antisemitic"
                if row.get("antisemitic") == 1
                else "preprocessed_tweets_not_antisemitic"
            )
            publisher.publish(topic, msg)
