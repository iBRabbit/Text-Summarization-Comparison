import pandas as pd
import string
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

import pickle

class LanguageDetection(object):
    model = None
    cv = CountVectorizer()
    le = LabelEncoder()
    
    def __init__(self):
        self.cv = pickle.load(open('models/lang_models/cv.pkl', 'rb'))
        self.le = pickle.load(open('models/lang_models/le.pkl', 'rb'))
        self.model = pickle.load(open('models/lang_models/model_language_detection.pkl', 'rb'))
        
    def remove_unwanted_char(self, text) : 
        text = re.sub(r'\d+', '', text)
        text = [i for i in text if i not in string.punctuation]
        text = ''.join(text)
        text = text.lower()
        return 

    def predict(self, text) :
        x = self.cv.transform([text]).toarray()
        lang = self.model.predict(x)
        lang = self.le.inverse_transform(lang)
        return lang[0]
