import json
import string
import pandas as pd
from  nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pandas.core.methods.to_dict import to_dict

from test_mongodb import load_data, convert_by_df


class InitialCleanText():
    def __init__(self):
        self.mongo = load_data()
        self.df = convert_by_df(self.mongo)
        # self.df:
    def remove_punctuation(self):
        self.df['clean_text'] = self.df['text'].str.replace(r'[{}]'.format(string.punctuation), '', regex=True)
        return self.df
    def remove_spaces(self):
        self.df['clean_text'] = self.df['clean_text'].str.replace(r'[^A-Za-z0-9\s]', '', regex=True)
        return self.df
    def remove_extra_whitespace(self):
        self.df['clean_text'] = self.df['clean_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
        return self.df
    def convert_text_to_lowercase(self):
        self.df['clean_text'] = self.df['clean_text'].apply(lambda x: x.lower())
        return self.df
    def division_text(self):
        self.df['list_words'] = self.df['clean_text'].str.split()
        return self.df
    def remove_stopwords(self):
        list_of_stopwords = stopwords.words('english')
        self.df['list_words'] = self.df['list_words'].apply(lambda x:[word for word in x if word not in list_of_stopwords])
        return self.df
    def find_root_of_word(self):
        ps = PorterStemmer()
        self.df['list_words'] = self.df['list_words'].apply(lambda x:[ps.stem(word) for word in x])
        return self.df
    def retrons_to_string(self):
        self.df['clean_text'] = self.df['list_words'].apply(lambda x:" ".join(x))
        return self.df
#
# clean = InitialCleanText()
# df = clean.remove_punctuation()
# df = clean.remove_spaces()
# df = clean.remove_extra_whitespace()
# df = clean.convert_text_to_lowercase()
# df = clean.division_text()
# df = clean.remove_stopwords()
# df = clean.find_root_of_word()
# df = clean.retrons_to_string()
# js = to_dict(df)
# print(df[['clean_text','text','list_words']].head())
# with open('file.txt', 'w') as f:
#     f.write(str(js))

# print(df['text','clean_text'].head())

#
# analyzer = Analyzer()
# analyzer.rarest_word()
# print(analyzer.find_weapon_name())