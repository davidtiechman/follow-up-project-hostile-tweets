import json
import os
import nltk
from nltk.sentiment import vader

from cleaning.app.processor import convert_by_df
from consumer.app.kafka_consumer import read_news


class CleaningEnricher:
    def __init__(self):
        self.mongo = read_news('raw_tweets_antisemitic', 3)
        self.js = [json.loads(i['message']) for i in self.mongo]
        self.df = convert_by_df(self.mongo)

    def emotion_text(self):
        nltk.download('vader_lexicon')  # Compute sentiment labels
        # tweet = self.df['Text'].loc[0]
        self.df['score'] = self.df['text'].apply(
            lambda text: vader.SentimentIntensityAnalyzer().polarity_scores(str(text))['compound'])
        self.df['type_text'] = self.df['score'].apply(
            lambda s: 'positive' if s >= 0.5 else ('negative' if s <= -0.5 else 'neutral'))
        self.df.drop(columns=['score'], inplace=True)
        return self.df


    def find_weapon_name(self):
        self.df['weapons_detected'] = self.df.apply(self.lop_of_array_weapons, axis=1)
        return self.df


    def lop_of_array_weapons(self,row):
        arr_weapon = []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, 'data', 'weapon_list (1).txt')
        with open(file_path, 'r') as file:
            arr_weapon = file.read().split('\n')
            arr_weapon = [w.lower() for w in arr_weapon]
        found_weapons = [w for w in arr_weapon if w in row['list_words']]
        return found_weapons if found_weapons else " "

# lop_of_array_weapons('')