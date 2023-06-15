import streamlit as st

from models.Frequency import Frequency
from models.TextRank import TextRank
from models.LanguageDetection import LanguageDetection

from helpers.Evaluation import Evaluation
from helpers.Files import Files

from io import StringIO

def get_summaries(file_name, text) :
    freq = Frequency()
    tr = TextRank()
    
    print("Generating summaries...")
    freq_summary = freq.summarize(file_name, text)
    tr_summary = tr.summarize(file_name, text)
    print(f"Summaries generated. Summaries saved in output directory (output/{file_name}))")
        
    return freq_summary, tr_summary

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

def get_language(text) :
    lang = LanguageDetection().predict(text)
    return lang

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
        
        uploaded_file.close()
    if selector == "Enter text" :
        
        st.subheader("Enter Text to Summarize")
        file_name = st.text_input("Enter File Name")
        
        text = st.text_area("Enter Text Here")
        
    if text == "" or file_name == "" :
        return

    if get_language(text) != 'English' :
        print("Language not supported. Please enter text in English")
        st.write("Language is probably not supported. The model is best suited for English. Please enter text in English")
        st.write("Language detected: " + get_language(text))
        return
    
    if len(text) < 100 :
        print("Text too short. Please enter text with more than 100 characters")
        st.write("Text too short. Please enter text with more than 100 characters")
        return
    
    freq_summary, tr_summary = get_summaries(file_name, text)
    
    models = {
        'Frequency': freq_summary,
        'TextRank': tr_summary
    }
    
    st.subheader("Frequency Summary")
    st.write(freq_summary)
    
    st.download_button(label="Download Frequency Summary", data=freq_summary, file_name=f"{file_name}_Frequency.txt")
    
    st.subheader("TextRank Summary")
    st.write(tr_summary)

    st.download_button(label="Download TextRank Summary", data=tr_summary, file_name=f"{file_name}_TextRank.txt")
    
    st.subheader("Evaluation based on original text")
    Evaluation().evaluate(models, text)    
    
    st.subheader("Credits")
    st.write("This project is made by:")
    st.write("1. Felix Prima - 2301899622")
    st.write("2. Bryan Felix - 2301925532")
    st.write("3. Irvin - 2301854555")
    
if __name__ == '__main__':
    main()
