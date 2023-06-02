from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

from helpers import file_helpers as fh

import math
import string

class Frequency:
    model_name = 'Frequency'
    
    stop_words = stopwords.words('english') + [p for p in string.punctuation]
    
    def generate_freq_matrix(self, sentences) : 
        freq_matrix = {}
        for sent in sentences :
            freq_table = {}
            words = word_tokenize(sent)
            stemmed_words = [PorterStemmer().stem(word) for word in words] # stemming
            
            for word in stemmed_words :
                word = word.lower() 
                
                if word in self.stop_words : # ignore stop words
                    continue
                
                if word in freq_table :
                    freq_table[word] += 1 # word already exists in sentence
                else :
                    freq_table[word] = 1 # first occurence of word in sentence
                    
            freq_matrix[sent[:15]] = freq_table # first 15 characters of sentence as key
        
        return freq_matrix
    
    def generate_TF_matrix(self, freq_matrix) :
        TF_matrix = {}
        for sent, freq_table in freq_matrix.items() :
            TF_table = {}
            total_words = len(freq_table)
            
            for word, count in freq_table.items() :
                TF_table[word] = count / total_words
                
            TF_matrix[sent] = TF_table
            
        return TF_matrix
    
    def generate_sent_per_words(self, freq_matrix) :
        '''
        How many sentences does a word occur in?
        '''
        sent_per_words = {}
        for sent, freq_table in freq_matrix.items() :
            for word, count in freq_table.items() :
                if word in sent_per_words :
                    sent_per_words[word] += 1
                else :
                    sent_per_words[word] = 1
        
        return sent_per_words
    
    def generate_IDF_matrix(self, freq_matrix, sent_per_words, total_sentences) :
        IDF_matrix = {}
        for sent, freq_table in freq_matrix.items() :
            IDF_table = {}
            
            for word in freq_table.keys() :
                IDF_table[word] = math.log10(total_sentences / float(sent_per_words[word]))
                
            IDF_matrix[sent] = IDF_table
            
        return IDF_matrix

    def generate_TF_IDF_matrix(self, TF_matrix, IDF_matrix) :
        TF_IDF_matrix = {}
        for (sent1, freq_table1), (_, freq_table2) in zip(TF_matrix.items(), IDF_matrix.items()) :
            TF_IDF_table = {}
            
            for (word1, TF), (_, IDF) in zip(freq_table1.items(), freq_table2.items()) :
                TF_IDF_table[word1] = TF * IDF
                
            TF_IDF_matrix[sent1] = TF_IDF_table
            
        return TF_IDF_matrix
    
    def get_sentence_score(self, TF_IDF_matrix) :
        sentence_value = {}
        for sent, freq_table in TF_IDF_matrix.items() :
            total_score = 0
            count = len(freq_table)
            
            for _, score in freq_table.items() :
                total_score += score
                
            sentence_value[sent] = total_score / count
            
        return sentence_value
    
    def get_average_score(self, sentence_value) :
        total_score = 0
        for _, score in sentence_value.items() :
            total_score += score
            
        return total_score / len(sentence_value)
    
    def generate_summary(self, sentences, sentence_value, threshold) :
        sentence_count = 0
        summary = ''
        for sent in sentences :
            if sent[:15] in sentence_value and sentence_value[sent[:15]] >= threshold :
                summary += ' ' + sent
                sentence_count += 1
                
        return summary
    
    def summarize(self, title, text) :
        sentences = sent_tokenize(text)
        total_sentences = len(sentences)
        freq_matrix = self.generate_freq_matrix(sentences)
        TF_matrix = self.generate_TF_matrix(freq_matrix)
        sent_per_words = self.generate_sent_per_words(freq_matrix)
        IDF_matrix = self.generate_IDF_matrix(freq_matrix, sent_per_words, total_sentences)
        TF_IDF_matrix = self.generate_TF_IDF_matrix(TF_matrix, IDF_matrix)
        sentence_value = self.get_sentence_score(TF_IDF_matrix)
        average_score = self.get_average_score(sentence_value)
        summary = self.generate_summary(sentences, sentence_value, 1.2 * average_score)
        
        fh.save_file(title, summary, self.model_name)
        return summary

