import gensim as gs
import string
import numpy as np

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from scipy import spatial as sp

class PageRank:
    stop_words = stopwords.words('english')
    
    def clean_sentence(self, sentence):
        cleaned_sentence = [word for word in sentence if word not in self.stop_words]
        cleaned_sentence = [word for word in cleaned_sentence if word not in string.punctuation]
        
        return cleaned_sentence
    
    def get_sentence_tokens(self, text):
        sentences = sent_tokenize(text)
        sentence_tokens = []
        for sentence in sentences:
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
    def summarize(self, text) :

        sentence_tokens = self.get_sentence_tokens(text)
        sentence_embeddings = self.get_sentence_embeddings(sentence_tokens)
        similarity_matrix = self.get_similarity_matrix(sentence_tokens, sentence_embeddings)
        print(similarity_matrix)
        
        
        
    pass

def main() :
    
    text='''Santiago is a Shepherd who has a recurring dream which is supposedly prophetic. Inspired on learning this, he undertakes a journey to Egypt to discover the meaning of life and fulfill his destiny. During the course of his travels, he learns of his true purpose and meets many characters, including an “Alchemist”, that teach him valuable lessons about achieving his dreams. Santiago sets his sights on obtaining a certain kind of “treasure” for which he travels to Egypt. The key message is, “when you want something, all the universe conspires in helping you to achieve it.” Towards the final arc, Santiago gets robbed by bandits who end up revealing that the “treasure” he was looking for is buried in the place where his journey began. The end.'''
    
    pr = PageRank()
    pr.summarize(text)
    
    pass
if __name__ == '__main__':
    main()
    