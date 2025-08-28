import string
from  nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from consumer.app.covert_to_df import convert_to_df

class InitialCleanText:
    def __init__(self,topic,num):
        self.df =  convert_to_df(topic,num)

    def remove_punctuation(self):
        "מוריד סימני פיסוק"
        self.df['clean_text'] = self.df['text'].str.replace(r'[{}]'.format(string.punctuation), '', regex=True)
        return self.df
    def remove_spaces(self):
        "מוריד סימנים מיוחדים"
        self.df['clean_text'] = self.df['clean_text'].str.replace(r'[^A-Za-z0-9\s]', '', regex=True)
        return self.df
    def remove_extra_whitespace(self):
        "מוסיר תווים לבנים מיותרים"
        self.df['clean_text'] = self.df['clean_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
        return self.df
    def convert_text_to_lowercase(self):
        "הופך את כל הטקסט לאותיות קטנות"
        self.df['clean_text'] = self.df['clean_text'].apply(lambda x: x.lower())
        return self.df
    def division_text(self):
        "מייצר עמודה בשם list wordsחדשה שמכיל את כל הטקסט מחולק למילים"
        self.df['list_words'] = self.df['clean_text'].str.split()
        return self.df
    def remove_stopwords(self):
        "מוריד מילות stopwords"
        list_of_stopwords = stopwords.words('english')
        self.df['list_words'] = self.df['list_words'].apply(lambda x:[word for word in x if word not in list_of_stopwords])
        return self.df
    def find_root_of_word(self):
        "הופך כל מילה לשורש שלו"
        ps = PorterStemmer()
        self.df['list_words'] = self.df['list_words'].apply(lambda x:[ps.stem(word) for word in x])
        return self.df
    def retrons_to_string(self):
        "מחזיר את רשימת המילים למחרוזת אחד"
        self.df['clean_text'] = self.df['list_words'].apply(lambda x:" ".join(x))
        return self.df
#
clean = InitialCleanText('raw_tweets_antisemitic',5)
df = clean.remove_punctuation()
df = clean.remove_spaces()
df = clean.remove_extra_whitespace()
df = clean.convert_text_to_lowercase()
df = clean.division_text()
df = clean.remove_stopwords()
df = clean.find_root_of_word()
df = clean.retrons_to_string()
# print(clean.df[])
# js = to_dict(df)
# print(df[['clean_text','text','list_words']].head())
# with open('file.txt', 'w') as f:
    # f.write(str(df))

# print(df['text','clean_text'].head())

#
# analyzer = Analyzer()
# analyzer.rarest_word()
# print(analyzer.find_weapon_name())