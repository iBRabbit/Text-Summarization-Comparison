# import models

import os

from models.Frequency import Frequency
from models.Pagerank import PageRank

from tests.Evaluation import Evaluation

from helpers.file_helpers import is_output_dir_exists

def get_summaries(file_name, text) :
    evaluation = Evaluation()
    freq = Frequency()
    pr = PageRank()
    
    if is_output_dir_exists : 
        freq_summary = open(f"output/{file_name}/Frequency.txt", 'r').read()
        pr_summary = open(f"output/{file_name}/PageRank.txt", 'r').read()
    else :
        freq_summary = freq.summarize(file_name, text)
        pr_summary = pr.summarize(file_name, text)
        
    return freq_summary, pr_summary


def main() :
    
    # In : file_name
    file_name = input("Enter file name : ")
    text = open(os.path.join(os.path.dirname(__file__), f"dataset/{file_name}.txt"), 'r').read()

    freq_summary, pr_summary = get_summaries(file_name, text)
    
    models = {
        'Frequency': freq_summary,
        'PageRank': pr_summary
    }
    
    evaluation = Evaluation()
    evaluation.evaluate(models, text)
    
    pass

if __name__ == '__main__':
    main()
    
