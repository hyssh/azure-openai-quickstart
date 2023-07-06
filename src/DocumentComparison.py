import os
import json
import dotenv
import openai
import json
import pandas as pd
import streamlit as st

# .env file must have OPENAI_API_KEY and OPENAI_API_BASE
dotenv.load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
ENGINE = os.environ.get("ENGINE", "chat-gpt")
TEMPERATURE = 0.1
MAX_TOKENS = 200
TOP_P = 1
FREQUENCY_PENALTY = 0.0
PRESENCE_PENALTY = 0.0

if "DocComparison" not in st.session_state:
    st.session_state["DocComparison"] = True


def load_contracts():
    #read two text files
    return open("./contract/version1.txt", "r").read(), open("./contract/version2.txt", "r").read()


def DocumentComairson():
    pass

# define custom function to run the openai.ChatCompletion.create function
def run(user_msg: str, system_msg: str):  
    """
    This function runs the openai.ChatCompletion.create function
    """
    messages = [{"role":"system", "content":system_msg},
                {"role":"user","content":user_msg}
                ]

    res = openai.ChatCompletion.create(
        engine=ENGINE,
        messages = messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
        n=1
        )
    
    return res.choices[0].message['content']

def DocumentComparison():
    """
    This function runs the openai.ChatCompletion.create function
    """

    system_msg = "You are contract reviewer. You are responsible for reviewing the contract and provide insights. When answer a question, start with simple conclusion and then explain in details with quotes from the contract."
    user_msg = ""


    # sidebar
    with st.sidebar:
        with st.container():
            st.info("Compare two documents. Type a question and click __Ask__ button to get answer.")
        sample_tab, system_tab = st.tabs(["samples", "system"])
        with sample_tab:
            st.write("## Sample Questions")
            st.code("what is the risk for the employee with the new updated version", language="html")
        with system_tab:
            st.write("## System Message")
            st.text_area(label="System", value=system_msg)

        
    # load documents
    ver1, ver2 = load_contracts()

    if st.session_state.DocComparison:
        st.markdown("---")
        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                with st.container():
                    st.write("### version 1")
                    v1_text_area = st.text_area(label="contents", value=ver1, height=500)
            with col2:
                with st.container():
                    st.write("### version 2")
                    v2_text_area = st.text_area(label="contents", value = ver2, height=500)
    else:
        pass

    st.markdown("---")

    with st.container():
        user_questions = st.text_input("Ask a question")
        if st.button("Ask"):
            st.spinner("Comparing...")
            user_msg = f"There are two dcouments. version 1 --- {v1_text_area} --- version 2 --- {v2_text_area} ---. Please compare the two documents and answer my question {user_questions}"
            with st.container():
                st.info(run(user_msg, system_msg))
        else:
            with st.container():
                st.empty()


if __name__ == "__main__":
    DocumentComparison()    