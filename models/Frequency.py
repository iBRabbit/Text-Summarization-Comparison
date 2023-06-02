from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import math
import string

class Frequency (object) :
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
            
            for word, score in freq_table.items() :
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
    
    def summarize(self, text) :
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
        print(summary)

def main() :
    freq = Frequency()
    text = '''Those Who Are Resilient Stay In The Game Longer
    "On the mountains of truth you can never climb in vain: either you will reach a point higher up today, or you will be training your powers so that you will be able to climb higher tomorrow." - Friedrich Nietzsche
    Challenges and setbacks are not meant to defeat you, but promote you. However, I realise after many years of defeats, it can crush your spirit and it is easier to give up than risk further setbacks and disappointments. Have you experienced this before? To be honest, I don't have the answers. I can't tell you what the right course of action is; only you will know. However, it's important not to be discouraged by failure when pursuing a goal or a dream, since failure itself means different things to different people. To a person with a Fixed Mindset failure is a blow to their self-esteem, yet to a person with a Growth Mindset, it's an opportunity to improve and find new ways to overcome their obstacles. Same failure, yet different responses. Who is right and who is wrong? Neither. Each person has a different mindset that decides their outcome. Those who are resilient stay in the game longer and draw on their inner means to succeed.
    I've coached many clients who gave up after many years toiling away at their respective goal or dream. It was at that point their biggest breakthrough came. Perhaps all those years of perseverance finally paid off. It was the 19th Century's minister Henry Ward Beecher who once said: "One's best success comes after their greatest disappointments." No one knows what the future holds, so your only guide is whether you can endure repeated defeats and disappointments and still pursue your dream. Consider the advice from the American academic and psychologist Angela Duckworth who writes in Grit: The Power of Passion and Perseverance: "Many of us, it seems, quit what we start far too early and far too often. Even more than the effort a gritty person puts in on a single day, what matters is that they wake up the next day, and the next, ready to get on that treadmill and keep going."
    I know one thing for certain: don't settle for less than what you're capable of, but strive for something bigger. Some of you reading this might identify with this message because it resonates with you on a deeper level. For others, at the end of their tether the message might be nothing more than a trivial pep talk. What I wish to convey irrespective of where you are in your journey is: NEVER settle for less. If you settle for less, you will receive less than you deserve and convince yourself you are justified to receive it.
    "Two people on a precipice over Yosemite Valley" by Nathan Shipps on Unsplash
    Develop A Powerful Vision Of What You Want
    "Your problem is to bridge the gap which exists between where you are now and the goal you intend to reach." - Earl Nightingale
    I recall a passage my father often used growing up in 1990s: "Don't tell me your problems unless you've spent weeks trying to solve them yourself." That advice has echoed in my mind for decades and became my motivator. Don't leave it to other people or outside circumstances to motivate you because you will be let down every time. It must come from within you. Gnaw away at your problems until you solve them or find a solution. Problems are not stop signs, they are advising you that more work is required to overcome them. Most times, problems help you gain a skill or develop the resources to succeed later. So embrace your challenges and develop the grit to push past them instead of retreat in resignation. Where are you settling in your life right now? Could you be you playing for bigger stakes than you are? Are you willing to play bigger even if it means repeated failures and setbacks? You should ask yourself these questions to decide whether you're willing to put yourself on the line or settle for less. And that's fine if you're content to receive less, as long as you're not regretful later.
    If you have not achieved the success you deserve and are considering giving up, will you regret it in a few years or decades from now? Only you can answer that, but you should carve out time to discover your motivation for pursuing your goals. It's a fact, if you don't know what you want you'll get what life hands you and it may not be in your best interest, affirms author Larry Weidel: "Winners know that if you don't figure out what you want, you'll get whatever life hands you." The key is to develop a powerful vision of what you want and hold that image in your mind. Nurture it daily and give it life by taking purposeful action towards it.
    Vision + desire + dedication + patience + daily action leads to astonishing success. Are you willing to commit to this way of life or jump ship at the first sign of failure? I'm amused when I read questions written by millennials on Quora who ask how they can become rich and famous or the next Elon Musk. Success is a fickle and long game with highs and lows. Similarly, there are no assurances even if you're an overnight sensation, to sustain it for long, particularly if you don't have the mental and emotional means to endure it. This means you must rely on the one true constant in your favour: your personal development. The more you grow, the more you gain in terms of financial resources, status, success - simple. If you leave it to outside conditions to dictate your circumstances, you are rolling the dice on your future.
    So become intentional on what you want out of life. Commit to it. Nurture your dreams. Focus on your development and if you want to give up, know what's involved before you take the plunge. Because I assure you, someone out there right now is working harder than you, reading more books, sleeping less and sacrificing all they have to realise their dreams and it may contest with yours. Don't leave your dreams to chance.
    '''
    freq.summarize(text)

if __name__ == '__main__':
    main()
