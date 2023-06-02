import gensim as gs
import string
import numpy as np
import networkx as nx

from helpers import file_helpers as fh

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from scipy import spatial as sp

class PageRank:
    stop_words = stopwords.words('english')
    model_name = 'PageRank'
    sentences = []
    
    def clean_sentence(self, sentence):
        cleaned_sentence = [word for word in sentence if word not in self.stop_words]
        cleaned_sentence = [word for word in cleaned_sentence if word not in string.punctuation]
        
        return cleaned_sentence
    
    def get_sentence_tokens(self, text):
        self.sentences = sent_tokenize(text)
        sentence_tokens = []
        for sentence in self.sentences:
            sentence_tokens.append(word_tokenize(sentence))
        
        for i in range(len(sentence_tokens)):
            sentence_tokens[i] = self.clean_sentence(sentence_tokens[i])
    
        return sentence_tokens
    
    
    def get_sentence_embeddings(self, sentence_tokens):
        '''
        Sentence embeddings adalah mengubah kalimat ke dalam angka numerik yang merepresentasikan kalimat tersebut
        
        sentence_tokens: list of list of words
        returns: list of embeddings
        '''
        
        model = gs.models.Word2Vec(sentence_tokens, min_count=1, epochs=1000, vector_size=1)
        
        sentence_embeddings = [[model.wv.get_index(word) for word in sentence] for sentence in sentence_tokens]
        
        max_length = max([len(tokens) for tokens in sentence_tokens])
        
        sentence_embeddings = [np.pad(emb, (0, max_length - len(emb)), 'constant') for emb in sentence_embeddings] # pad embeddings to make them of equal length
        return sentence_embeddings
    
    def get_similarity_matrix(self, sentence_tokens, sentence_embeddings):
        simliarity_matrix = np.zeros([len(sentence_tokens), len(sentence_tokens)])
        
        for i, re in enumerate(sentence_embeddings) :
            for j, ce in enumerate(sentence_embeddings) :
                simliarity_matrix[i, j] = 1 - sp.distance.cosine(re, ce)
        
        return simliarity_matrix
    
    def get_score(self, similarity_matrix):
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        return scores
    
    def get_top_sentence(self, scores):
        top_sentence = {sentence:scores[index] for index,sentence in enumerate(self.sentences)}
        top_sentence = dict(sorted(top_sentence.items(), key=lambda x: x[1], reverse=True)[:4])
        return top_sentence
        
    def generate_summary(self, top_sentences):
        summary = ''
        
        for sent in self.sentences:
            if sent in top_sentences.keys():
                summary += ' ' + sent
        return summary
    
    def summarize(self, title, text) :
        sentence_tokens = self.get_sentence_tokens(text)
        sentence_embeddings = self.get_sentence_embeddings(sentence_tokens)
        similarity_matrix = self.get_similarity_matrix(sentence_tokens, sentence_embeddings)
        scores = self.get_score(similarity_matrix)
        top_sentence = self.get_top_sentence(scores)
        summary = self.generate_summary(top_sentence)

        fh.save_file(title, summary, self.model_name)
        return summary
