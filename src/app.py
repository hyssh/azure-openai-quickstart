import streamlit as st
from NLP101 import sample101
from NLP102 import sample102
from NLP103 import sample103
from DocumentComparison import DocumentComparison
from SentimentAnalysis import SentimentAnalysis
from FacilityRequest import FacilityRequest


# create a single page application
st.set_page_config(page_title="Azure OpenAI demo", page_icon=":robot_face:", layout="wide")

# show option to chose detail page
st.sidebar.write("# Azure OpenAI demo")
# Add a link to github source code
st.sidebar.markdown("## Source code [@hyssh](https://github.com/hyssh/azure-openai-quickstart/tree/main/src)")
sample = st.sidebar.selectbox("Choose a scenario", ["Natural Language to SQL Query", "Generate Additional Insights", "LangChain SQL Agent", "Documents Comparison", "Sentiment Analysis", "Facility Request"], index=0)

if sample == "Natural Language to SQL Query":
    sample101()
elif sample == "Generate Additional Insights":
    sample102()
elif sample == "LangChain SQL Agent":
    sample103()
elif sample == "Documents Comparison":
    DocumentComparison()
elif sample == "Sentiment Analysis":
    SentimentAnalysis()
elif sample == "Facility Request":
    FacilityRequest()