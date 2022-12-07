from spellchecker import SpellChecker
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from math import sqrt, floor
from collections import defaultdict, Counter

class PreProcessor:

    stopwords = set(word for words in map(lambda w:re.split('\W+', w), list(stopwords.words('english'))) for word in words)
    porter_stemmer = nltk.PorterStemmer()
    spell = SpellChecker()
   
    def to_lower_case(self, string):
        return string.lower()
    
    def remove_special_characters(self, string):
        return re.sub('\W+', ' ', string)
    
    def remove_excess_whitespace(self, string):
        return re.sub(' +', ' ', string.strip())
    
    def tokenize_data(self, string):
        return string.split(' ')

    def remove_stop_words(self, string):
        return list(self.stem_word(PreProcessor.spell.correction(word) or word) for word in string if word not in self.stopwords)
    
    def stem_word(self, word):
        return PreProcessor.porter_stemmer.stem(word)
    
    def pre_process_string(self, string):
        string = self.to_lower_case(string)
        string = self.remove_special_characters(string)
        string = self.remove_excess_whitespace(string)
        string = self.tokenize_data(string)
        string = self.remove_stop_words(string)
        return string