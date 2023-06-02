import os

class Files:
    OUTPUT_DIR = 'output'

    def is_output_dir_exists(self, title) : 
        return os.path.isdir(f"{self.OUTPUT_DIR}/{title}")

    def save_file(self, title, content, model_name) : 
        
        if not os.path.isdir(self.OUTPUT_DIR) :
            os.makedirs(self.OUTPUT_DIR)
        
        if not self.is_output_dir_exists(title) : 
            os.makedirs(f"{self.OUTPUT_DIR}/{title}")
        
        with open(f"{self.OUTPUT_DIR}/{title}/{model_name}.txt", 'w') as f : 
            f.write(content)