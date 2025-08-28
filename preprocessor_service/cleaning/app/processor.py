import json
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from preprocessor_service.consumer.app.kafka_consumer import read_news
import pandas as pd
# from test_mongodb import convert_by_df

# Function to convert a Mongo-like list of messages into a pandas DataFrame
def convert_by_df(mongo):
    mongo = list(mongo)  # ensure it's a list
    df = pd.DataFrame(mongo)  # convert to DataFrame
    return df

# Class responsible for cleaning and preprocessing text
class InitialCleanText:
    def __init__(self, mongo):
        self.mongo = mongo  # raw messages
        self.js = [json.loads(i['message']) for i in self.mongo]  # parse JSON messages
        self.df = convert_by_df(self.mongo)  # convert messages to DataFrame

    # Remove punctuation characters from the text
    def remove_punctuation(self):
        self.df['clean_text'] = self.df['text'].str.replace(r'[{}]'.format(string.punctuation), '', regex=True)
        return self.df

    # Remove non-alphanumeric characters (except spaces)
    def remove_spaces(self):
        self.df['clean_text'] = self.df['clean_text'].str.replace(r'[^A-Za-z0-9\s]', '', regex=True)
        return self.df

    # Remove extra whitespace, tabs, newlines
    def remove_extra_whitespace(self):
        self.df['clean_text'] = self.df['clean_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
        return self.df

    # Convert all text to lowercase
    def convert_text_to_lowercase(self):
        self.df['clean_text'] = self.df['clean_text'].apply(lambda x: x.lower())
        return self.df

    # Split text into list of words
    def division_text(self):
        self.df['list_words'] = self.df['clean_text'].str.split()
        return self.df

    # Remove stopwords (common words like "the", "and", etc.)
    def remove_stopwords(self):
        list_of_stopwords = stopwords.words('english')
        self.df['list_words'] = self.df['list_words'].apply(lambda x: [word for word in x if word not in list_of_stopwords])
        return self.df

    # Apply stemming to reduce words to their root form
    def find_root_of_word(self):
        ps = PorterStemmer()
        self.df['list_words'] = self.df['list_words'].apply(lambda x: [ps.stem(word) for word in x])
        return self.df

    # Convert the list of words back into a single cleaned string
    def retrons_to_string(self):
        self.df['clean_text'] = self.df['list_words'].apply(lambda x: " ".join(x))
        return self.df

