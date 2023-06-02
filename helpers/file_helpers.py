import os

OUTPUT_DIR = 'output'

def is_output_dir_exists(title) : 
    return os.path.isdir(f"{OUTPUT_DIR}/{title}")

def save_file(title, content, model_name) : 
    
    if not os.path.isdir(OUTPUT_DIR) :
        os.makedirs(OUTPUT_DIR)
    
    if not is_output_dir_exists(title) : 
        os.makedirs(f"{OUTPUT_DIR}/{title}")
    
    with open(f"{OUTPUT_DIR}/{title}/{model_name}.txt", 'w') as f : 
        f.write(content)