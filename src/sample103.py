#
# https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602/38
#
import os
import openai
import dotenv
import pandas as pd
import streamlit as st
from sqldbconn import get_connx
from langchain.agents import create_sql_agent
from typing import Dict, Union, Any, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import AgentExecutor
from sqldbconn import get_connection_string
from langchainadapters import HtmlCallbackHandler


# .env file must have OPENAI_API_KEY and OPENAI_API_BASE
dotenv.load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

callback_mycustomhandler = HtmlCallbackHandler()

db = SQLDatabase.from_uri(get_connection_string())

# tables = db.get_usable_table_names()

llm = AzureChatOpenAI(deployment_name="chatgpt",temperature=0, max_tokens=500)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, use_query_checker=True)

_DEFAULT_TEMPLATE =  """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

SalesLT.Address(AddressID, AddressLIne1, AddressLine2, City, StateProvince, CountryRegion, PostalCode, rowguid, modifiedDate)
SalesLT.Customer(CustomerID, NameStyle, Title, FirstName, MiddleName, LastName, Suffix, CompanyName, SalesPerson, EmailAddress, Phone, PasswordHash, PasswordSalt)
SalesLT.CustomerAddress(CustomerID, AddressID, AddressType)
SalesLT.Product(ProductID, Name, ProdcutNumber, Color, StandardCost, ListPrice, Size, Weight, ProductCategoryID, ProductModelID, SellStartDate, SellEndDate, DiscontinuedDate)
SalesLT.ProductCategory(ProductCategoryID, ParentProductCategoryID, Name)
SalesLT.ProdcutDescription(ProductDescriptionID, Description)
SalesLT.ProductModel(ProductModelID, Name, CatalogDesciortion)
SalesLT.ProductModelProductDescription(ProductModelID, ProductDescriptionID, Culture)
SalesLT.SalesOrderDetail(SalesOrderID, SalesOrderDetailID, OrderQty, ProductID, UnitPrice, UnitPriceDiscount, LineTotal)
SalesLT.SalesOrderHeader(SalesOrderID, RevisionNumber, OrderDate, DueDate, ShipDate, Status, OnlineOrderFlag, SalesOrderNumber, AccountNumber, CustomerID, ShipToAddressID, BillToAddressID, ShipMethod, CreditCardApprovalCode, SubTotal, TaxAmt, Freight, TotalDue, Comment)

If someone asks for the table foobar, they really mean the employee table.

Question:
"""

# PROMPT = PromptTemplate(
#     input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
# )
# db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)




user_input = st.text_input("Enter your question here", value="How many orders are there in the order details table?")

if user_input:
        agent_executor = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                verbose=True,
                prefix=_DEFAULT_TEMPLATE,
                top_k=10
        )

        st.write(agent_executor.run(user_input))