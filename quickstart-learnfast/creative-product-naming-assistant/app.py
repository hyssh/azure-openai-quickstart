import os
import json
import dotenv
import openai
import streamlit as st
from streamlit_chat import message


# .env file must have OPENAI_API_KEY and OPENAI_API_BASE
dotenv.load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

system_msg = """
You're a creative and detail-oriented Product Naming Specialist. 
You're responsible for developing and executing naming strategies for our products and services. 
You have a deep understanding of brand identity and positioning, as well as experience in developing compelling and memorable product names.
"""

examples = """
"""

ENGINE = "chatgpt"
TEMPERATURE = 0.9
MAX_TOKENS = 200
TOP_P = 1
FREQUENCY_PENALTY = 1.0
PRESENCE_PENALTY = 1.0


st.set_page_config(page_title="Creative Product Naming Assistant", page_icon=":robot_face:", layout="wide", initial_sidebar_state="collapsed")

if "IsBegin" not in st.session_state:
    st.session_state["IsBegin"] = False

if "history_conversations" not in st.session_state:
    st.session_state["history_conversations"] = []

st.write("# Creative Product Naming Assistant")

# define custom function to run the openai.ChatCompletion.create function
def run(history: list or None, user_msg: str):
    if history is None:
        messages = [{"role":"system", "content":system_msg}, {"role":"user","content":user_msg}]
        st.session_state.history_conversations.append({"role":"system", "content":system_msg})
        st.session_state.history_conversations.append({"role":"user","content":user_msg})
    else:
        messages = history + [{"role":"user","content":user_msg}]
        st.session_state.history_conversations.append({"role":"user","content":user_msg})

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
    
    st.session_state.history_conversations.append({"role":"assistant", "content":res.choices[0].message['content']})
    

# sidebar for system messages and examples
with st.sidebar:
    examples_tab, system_tab = st.tabs(["examples", "system"])
    # samples
    with examples_tab:
        st.header("Examples")
        examples = st.text_input(label="Add examples")

    with system_tab:
        st.header("System messages")
        system_msg = st.text_area(label="Edit system message", value=system_msg)

# display history conversations
with st.container():
    # create a input using streamlit
    user_msg = st.text_input(label="Type your message here", value="")

    # create a button using streamlit
    if st.button("Send"):
        if st.session_state["IsBegin"] == False:
            st.session_state["IsBegin"] = True
            run(history = None, user_msg = user_msg)
        else:
            run(history = st.session_state.history_conversations, user_msg = user_msg)

if st.session_state["IsBegin"] == True:
    # display history conversations in reverse order
    for i in range(len(st.session_state.history_conversations)-1, -1, -1):
        if st.session_state.history_conversations[i]["role"] == "user":
            message(st.session_state.history_conversations[i]["content"], is_user=True, key=str(i))
        elif st.session_state.history_conversations[i]["role"] == "assistant":
            message(st.session_state.history_conversations[i]["content"], key=str(i))
        elif st.session_state.history_conversations[i]["role"] == "system":
            message(st.session_state.history_conversations[i]["content"], key=str(i))

with st.container():
    st.info(st.session_state.history_conversations)
    if len(st.session_state.history_conversations) > 0:
        # download chat history as json file 
        # download as json file
        st.download_button(label="Save chat history", data=json.dumps(st.session_state.history_conversations), file_name="chat_history.json", mime="application/json")