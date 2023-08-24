import streamlit as st
from NLP101 import sample101
from NLP102 import sample102
from NLP103 import sample104
from DocumentComparison import DocumentComparison
from SentimentAnalysis import SentimentAnalysis


# create a single page application
st.set_page_config(page_title="Azure OpenAI demo", page_icon=":robot_face:", layout="wide")

# show option to chose detail page
st.sidebar.write("# Azure OpenAI demo")
sample = st.sidebar.selectbox("Choose a scenario", ["NLP-Basic", "NLP-Intermediate", "NLP-Advanced", "DocumentComparison", "SentimentAnalysis"], index=0)

if sample == "NLP-Basic":
    sample101()
elif sample == "NLP-Intermediate":
    sample102()
elif sample == "NLP-Advanced":
    sample104()
elif sample == "DocumentComparison":
    DocumentComparison()
elif sample == "SentimentAnalysis":
    SentimentAnalysis()