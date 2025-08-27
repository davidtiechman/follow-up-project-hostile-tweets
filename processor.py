from nltk.sentiment import vader
import os
import string
import re
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class CleanText():
    def __init__(self):
        self.df = ''
        # self.df:
        # self.df:
    def remove_punctuation(self):
        self.df['clene_data'] = self.df['Text'].str.translate(str.maketrans('', '', string.punctuation))
        return self.df
    def remove_spaces(self):
        self.df['clene_data'] = self.df['Text'].str.replace(r'[^A-Za-z-9\s]', '', regex=True)
        return self.df
    def remove_extra_whitespace(self):
        pass
    def remove_stopwords(self):
        pass
    def convert_text_to_lowercase(self):
        pass
    def find_root_of_word(self):
        pass

    def rarest_word(self):
        self.df['array_text'] = self.df['Text'].str.split(" ")
        self.df['rarest_word'] = self.df['array_text'].apply(lambda words: Counter(words).most_common()[-1][0])
        return self.df

    def emotion_text(self):
        nltk.download('vader_lexicon')  # Compute sentiment labels
        # tweet = self.df['Text'].loc[0]
        self.df['score'] = self.df['Text'].apply(lambda text: vader.SentimentIntensityAnalyzer().polarity_scores(str(text))['compound'])
        self.df['type_text'] = self.df['score'].apply(lambda s: 'positive' if s >= 0.5 else ('negative' if s <= -0.5 else 'neutral'))
        self.df.drop(columns=['score'], inplace=True)
        return self.df

    def find_weapon_name(self):
        self.df['weapons_detected'] = self.df.apply(self.lop_of_array_weapons, axis=1)
        return self.df
    def lop_of_array_weapons(self,row):
        arr_weapon = []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, 'data', 'weapon_list.txt')

        with open(file_path, 'r') as file:
            arr_weapon = file.read().split('\n')
        for w in arr_weapon:
            if w in row['array_text']:
                return w
        return ""



#
# analyzer = Analyzer()
# analyzer.rarest_word()
# print(analyzer.find_weapon_name())