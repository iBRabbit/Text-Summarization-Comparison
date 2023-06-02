# import models

import os

from models.Frequency import Frequency
from models.Pagerank import PageRank

from tests.Evaluation import Evaluation

from helpers.file_helpers import is_output_dir_exists

def get_summaries(file_name, text) :
    freq = Frequency()
    pr = PageRank()
    
    if is_output_dir_exists(file_name) : 
        print(f"Summaries already generated. Summaries loaded from output directory (output/{file_name})")
        freq_summary = open(f"output/{file_name}/Frequency.txt", 'r').read()
        pr_summary = open(f"output/{file_name}/PageRank.txt", 'r').read()
        
    else :
        print("Generating summaries...")
        freq_summary = freq.summarize(file_name, text)
        pr_summary = pr.summarize(file_name, text)
        print(f"Summaries generated. Summaries saved in output directory (output/{file_name}))")
        
    return freq_summary, pr_summary


def main() :
    
    # In : file_name
    file_name = input("Enter file name : ")
    
    try:
        text = open(os.path.join(os.path.dirname(__file__), f"dataset/{file_name}.txt"), 'r').read()
    except :
        print("File not found")
        return

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
    
