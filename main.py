import streamlit as st
import os

from models.Frequency import Frequency
from models.Pagerank import PageRank

from helpers.Evaluation import Evaluation
from helpers.Files import Files

from io import StringIO

def get_summaries(file_name, text) :
    freq = Frequency()
    pr = PageRank()
    
    if Files().is_output_dir_exists(file_name) : 
        print(f"Summaries already generated. Summaries loaded from output directory (output/{file_name})")
        freq_summary = open(f"output/{file_name}/Frequency.txt", 'r').read()
        pr_summary = open(f"output/{file_name}/PageRank.txt", 'r').read()
        
    else :
        print("Generating summaries...")
        freq_summary = freq.summarize(file_name, text)
        pr_summary = pr.summarize(file_name, text)
        print(f"Summaries generated. Summaries saved in output directory (output/{file_name}))")
        
    return freq_summary, pr_summary

def is_file_valid(uploaded_file) :
    if uploaded_file is None :
        print("File not found. Please upload a file")
        st.write("File not found. Please upload a file")
        return False

    if uploaded_file.name.split('.')[-1] != 'txt' :
        print(uploaded_file)
        print("Please upload a TXT file")
        st.write("Please upload a TXT file")
        return False
    
    return True


def main() :
    
    st.title("Text Summarization")
    st.subheader("Select an option to summarize text")
    selector = st.selectbox("Select your choice", ["Select", "Upload a file", "Enter text"])
    
    if selector == "Select" :
        return
    
    if selector == "Upload a file" :
        st.subheader("Upload File to Summarize")
        
        uploaded_file = st.file_uploader('Upload a TXT File')
        
        if not is_file_valid(uploaded_file):
            return  
        
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        file_name = uploaded_file.name.split('.')[0]
        text = stringio.read()
        
        st.write("File Uploaded Successfully")
        
        freq_summary, pr_summary = get_summaries(file_name, text)
        
        models = {
            'Frequency': freq_summary,
            'PageRank': pr_summary
        }
        
        Evaluation().evaluate(models, text)    
        
        st.download_button(label="Download Frequency Summary", data=freq_summary, file_name=f"{file_name}_Frequency.txt")
        st.download_button(label="Download PageRank Summary", data=pr_summary, file_name=f"{file_name}_PageRank.txt")
        return 
    
    if selector == "Enter text" :
        
        st.subheader("Enter Text to Summarize")
        file_name = st.text_input("Enter File Name")
        
        text = st.text_area("Enter Text Here")
        
        if text == "" or file_name == "" :
            return
        
        freq_summary, pr_summary = get_summaries(file_name, text)
        
        models = {
            'Frequency': freq_summary,
            'PageRank': pr_summary
        }
        
        Evaluation().evaluate(models, text)    
        
        st.download_button(label="Download Frequency Summary", data=freq_summary, file_name=f"{file_name}_Frequency.txt")
        st.download_button(label="Download PageRank Summary", data=pr_summary, file_name=f"{file_name}_PageRank.txt")
        return
        
if __name__ == '__main__':
    main()
