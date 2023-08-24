#
# https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602/38
# https://python.langchain.com/docs/modules/chains/popular/sqlite
#
import os
import openai
import dotenv
import asyncio
import pandas as pd
import streamlit as st
from sqldbconn import get_connection_string
from typing import Dict, Union, Any, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.schema import AgentAction, AgentFinish, LLMResult
from concurrent.futures import ThreadPoolExecutor
from langchain.agents import AgentExecutor, initialize_agent, AgentType

import asyncio
from concurrent.futures import ThreadPoolExecutor

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.llms import AzureOpenAI
from langchain.sql_database import SQLDatabase

from dotenv import load_dotenv
import openai
import os
from typing import Any, Dict, Union

# .env file must have OPENAI_API_KEY and OPENAI_API_BASE
dotenv.load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("MODEL_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")

class StdOutCallbackHandler(BaseCallbackHandler):    
    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        pass

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        pass

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        #  asyncio.run(st.info(f"\u2611 {action} ..."))
        if "Action Input" in action.log:
            action = action.log.split("Action Input:")[1]
            asyncio.run(st.info(f"\u2611 Searching: {action} ..."))


def sample104():
    db = SQLDatabase.from_uri(get_connection_string())
    llm = AzureOpenAI(deployment_name=DEPLOYMENT_NAME, model_name=MODEL_NAME, temperature=0.0, max_tokens=512, top_p=0.0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        return_intermediate_steps=True,
        callback_manager=CallbackManager(handlers=[StdOutCallbackHandler()])
    )

    with st.sidebar:
        with st.container():
            st.info("This sample use LangChain sql agent which repeats [Action > Observation > Thought] steps to finalize the answer")
        st.write("## Sample Questions")
        st.code("high-value customers for targeted marketing campaigns or loyalty programs", language="html")
        st.code("average number of orders and purchase amount per customer ", language="html")
        st.code("Get top 5 most popular products with the amount of the purchases", language="html")
        st.code("Get customer email and address who purchased our products the most with the amount of the purchases", language="html")
        st.code("Create a list combining product category and product naming it 'ProductShortDesc' name and add sales revenue", language="html")

    # main page
    st.write("# Natual Language to SQL Query #103")

    user_input = st.text_input("Type your question about World Wide Importers database here")

    # if user_input:
    #     with st.spinner("Loading..."):
    #         results = agent_executor(user_input)                
    #         if "output" in results:
    #             st.write(results["output"])
    #         elif "Final Answer" in results:
    #             st.write(results["Final Answer"])
    #         else:
    #             st.warning("No answer found")

    if user_input:
        with st.spinner("Loading..."):
            results = agent_executor(user_input)
            st.write(results)


if __name__ == "__main__":
        sample104()