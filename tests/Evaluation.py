from rouge import Rouge

class Evaluation :
    def get_evaluation_score(self, summary_text, original_text) : 
        rouge = Rouge()
        score = rouge.get_scores(summary_text, original_text, avg=True)
        return score
    
    def evaluate(self, models, original_text) : 
        for model_name, summary in models.items() :
            scores = self.get_evaluation_score(summary, original_text)
            print(f"Rouge-l F1 score for {model_name} : {scores['rouge-l']['f'] * 100}%")