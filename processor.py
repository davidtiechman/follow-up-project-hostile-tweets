import string
from  nltk.corpus import stopwords
from nltk.stem import PorterStemmer
class InitialCleanText():
    def __init__(self):
        self.df = ''
        # self.df:
        # self.df:
    def remove_punctuation(self):
        self.df['clene_data'] = self.df['Text'].str.translate(str.maketrans('', '', string.punctuation))
        return self.df
    def remove_spaces(self):
        self.df['clean_text'] = self.df['Text'].str.replace(r'[^A-Za-z0-9\s]', '', regex=True)
        return self.df
    def remove_extra_whitespace(self):
        self.df['clean_text'] = self.df['Text'].str.translate(r'\s+', ' ', regex=True).str.strip()
        return self.df
    def convert_text_to_lowercase(self):
        self.df['clean_text'].aplly(lambda x: x.lower())
        return self.df
    def division_text(self):
        self.df['text_division'] = self.df['clean_text'].split()
        return self.df
    def remove_stopwords(self):
        list_of_stopwords = stopwords.words('english')
        self.df['list_words'].apply(lambda x:[word for word in x if word not in list_of_stopwords])
        pass
    def find_root_of_word(self):
        ps = PorterStemmer()
        self.df['list_words'].apply(lambda x:[ps.stem(word) for word in x])
        return self.df
    def retrons_to_string(self):
        self.df['clean_text'] = " ".join(self.df['list_words'])



#
# analyzer = Analyzer()
# analyzer.rarest_word()
# print(analyzer.find_weapon_name())