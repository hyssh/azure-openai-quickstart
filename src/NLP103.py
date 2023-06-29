#
# https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602/38
# https://python.langchain.com/docs/modules/chains/popular/sqlite
#
import os
import openai
import dotenv
import pandas as pd
import streamlit as st
from sqldbconn import get_connection_string
from typing import Dict, Union, Any, List
# # from langchain import OpenAI
# from langchain.llms import AzureOpenAI
# from langchain import SQLDatabase
# from langchain.chains import SQLDatabaseSequentialChain, SQLDatabaseChain
# from langchain.prompts.prompt import PromptTemplate
# from langchain.schema import AgentAction
# from langchain.sql_database import SQLDatabase
# from langchain.chat_models import AzureChatOpenAI
# from langchain.agents import AgentExecutor
# from langchain.agents import create_sql_agent
# from langchain.llms.openai import AzureOpenAI
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchainadapters import HtmlCallbackHandler
# from langchain.callbacks.base import BaseCallbackHandler

# .env file must have OPENAI_API_KEY and OPENAI_API_BASE
dotenv.load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("MODEL_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")

def sample103():
        from langchain.llms import AzureOpenAI
        from langchain import SQLDatabase
        from langchain.chains import SQLDatabaseSequentialChain, SQLDatabaseChain
        from langchain.prompts.prompt import PromptTemplate

        db = SQLDatabase.from_uri(get_connection_string())
        llm = AzureOpenAI(deployment_name=DEPLOYMENT_NAME, model_name=MODEL_NAME, temperature=0.0, max_tokens=512, top_p=0.0)

        _DEFAULT_TEMPLATE =  """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Do not add any additional information to the answer. 
        Do not add any additional questions to the answer.

        Only use the following tables:
        {table_info}

        Use the following format:
        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"
        Answer: "Final answer here"
                
        Question:{input}
        """

        with st.sidebar:
            LANGCHAINTYPE = st.radio("Select Chain Type", ["SQLDatabaseChain", "SQLDatabaseSequentialChain"])
            RETURN_STEPS = st.checkbox("Return Intermediate Steps", value=True)
            st.write("## Sample Questions")
            st.code("high-value customers for targeted marketing campaigns or loyalty programs", language="html")
            st.code("average number of orders and purchase amount per customer ", language="html")
            st.code("Get top 5 most popular products with the amount of the purchases", language="html")
            st.code("Get customer email and address who purchased our products the most with the amount of the purchases", language="html")
            st.code("Create a list combining product category and product naming it 'ProductShortDesc' name and add sales revenue", language="html")

        st.write("# Natual Language to SQL Query #103")

        user_input = st.text_input("Enter your question here")

        if RETURN_STEPS:
            if user_input:
                    with st.spinner("Loading..."):
                            PROMPT = PromptTemplate(input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE)
                            if LANGCHAINTYPE == "SQLDatabaseChain":
                                    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, return_intermediate_steps=True)
                                    results = db_chain(user_input)
                                    st.write(results["result"])
                                    with st.expander("See details"):
                                            # st.write(_parse_example(results))
                                            st.write(results)
                            else:
                                    chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)
                                    results = chain(user_input)
                                    st.write(results["result"])
                                    with st.expander("See details"):
                                            st.json(results)
                                            # st.write(_parse_example(results))
                                            st.markdown("```SQL"+results["intermediate_steps"][1]+"```")
                                            # st.table(pd.DataFrame(eval(results["intermediate_steps"][3])))
        else:
            if user_input:
                    with st.spinner("Loading..."):
                            PROMPT = PromptTemplate(input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE)
                            if LANGCHAINTYPE == "SQLDatabaseChain":
                                    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)
                                    results = db_chain.run(user_input)
                                    st.write(results)
                            else:
                                    chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=True )
                                    results = chain.run(user_input)
                                    st.write(results)
    

def _parse_example(result: Dict) -> Dict:
    sql_cmd_key = "sql_cmd"
    sql_result_key = "sql_result"
    table_info_key = "table_info"
    input_key = "input"
    final_answer_key = "answer"

    _example = {
        "input": result.get("query"),
    }

    steps = result.get("intermediate_steps")
    answer_key = sql_cmd_key # the first one
    for step in steps:
        # The steps are in pairs, a dict (input) followed by a string (output).
        # Unfortunately there is no schema but you can look at the input key of the
        # dict to see what the output is supposed to be
        if isinstance(step, dict):
            # Grab the table info from input dicts in the intermediate steps once
            if table_info_key not in _example:
                _example[table_info_key] = step.get(table_info_key)

            if input_key in step:
                if step[input_key].endswith("SQLQuery:"):
                    answer_key = sql_cmd_key # this is the SQL generation input
                if step[input_key].endswith("Answer:"):
                    answer_key = final_answer_key # this is the final answer input
            elif sql_cmd_key in step:
                _example[sql_cmd_key] = step[sql_cmd_key]
                answer_key = sql_result_key # this is SQL execution input
        elif isinstance(step, str):
            # The preceding element should have set the answer_key
            _example[answer_key] = step
    return _example

def sample104():
    from langchain.agents import create_sql_agent
    from langchain.agents.agent_toolkits import SQLDatabaseToolkit
    from langchain.sql_database import SQLDatabase
    from langchain.agents.agent_types import AgentType
    from langchain.llms import AzureOpenAI

    db = SQLDatabase.from_uri(get_connection_string())
    llm = AzureOpenAI(deployment_name=DEPLOYMENT_NAME, model_name=MODEL_NAME, temperature=0.0, max_tokens=256, top_p=0.0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        return_intermediate_steps=True,
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

    if user_input:
          with st.spinner("Loading..."):
                results = agent_executor(user_input)
                
                st.write(results["output"])
                with st.expander("See details"):
                      st.write(results)


if __name__ == "__main__":
        # sample103()
        sample104()