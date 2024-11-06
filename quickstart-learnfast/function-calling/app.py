import os
import random
import gradio as gr
import openai
import json
import requests
import pytz
from sqldbconn import get_connx
from datetime import datetime
from dotenv import load_dotenv
import requests
from collections import OrderedDict

env_path = "/.env"
load_dotenv(dotenv_path=env_path, override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
ENGINE = os.getenv("ENGINE")
bing_search_url = os.getenv("BING_SEARCH_API_BASE")
os.environ['AZURE_SEARCH_ENDPOINT'] = os.getenv("AZURE_SEARCH_ENDPOINT")

def search_bing(query):
    headers = {"Ocp-Apim-Subscription-Key": os.getenv("BING_SEARCH_API_KEY")}
    params = {"q": query, "textDecorations": False }
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    output = []

    for result in search_results['webPages']['value']:
        output.append({
            'title': result['name'],
            'link': result['url'],
            'snippet': result['snippet']
        })

    return json.dumps(output)

def pci_dss_v4(query)->str:
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    search_key = os.getenv("AZURE_SEARCH_KEY"); 
    index = os.getenv("AZURE_SEARCH_INDEX_NAME")
    search_api_version = os.getenv("AZURE_SEARCH_API_VERSION")    
    headers = {'Content-Type': 'application/json','api-key': search_key}
    params = {'api-version': search_api_version}
    k = 5
    reranker_threshold =1

    agg_search_results = dict()

    search_payload = {
        "search": query,
        "queryType": "semantic",
        "semanticConfiguration": "my-semantic-config",
        "count": "true",
        "speller": "lexicon",
        "queryLanguage": "en-us",
        "captions": "extractive",
        "answers": "extractive",
        "top": k
    }

    search_payload["select"]= "id, title, content, name, location"
    

    resp = requests.post(search_endpoint+ "/indexes/" + index + "/docs/search",
                        data=json.dumps(search_payload), headers=headers, params=params)

    search_results = resp.json()
    agg_search_results[index] = search_results

    content = dict()
    ordered_content = OrderedDict()
    
    for index,search_results in agg_search_results.items():
        for result in search_results['value']:
            if result['@search.rerankerScore'] > reranker_threshold: # Show results that are at least N% of the max possible score=4
                content[result['id']]={
                                        "title": result['title'], 
                                        "name": result['name'], 
                                        "location": result['location'],
                                        "caption": result['@search.captions'][0]['text'],
                                        "index": index
                                    }
                content[result['id']]["content"]= result['content']
                content[result['id']]["score"]= result['@search.score'] # Uses the Hybrid RRF score
                
    # After results have been filtered, sort and add the top k to the ordered_content
        
    count = 0  # To keep track of the number of results added
    for id in sorted(content, key=lambda x: content[x]["score"], reverse=True):
        ordered_content[id] = content[id]
        count += 1
        if count >= k:  # Stop after adding k results
            break

    return json.dumps(ordered_content)

def retrieve_sales_report(query)->str:
    # Your implementation here
    import json
    import pandas as pd
    from sqldbconn import get_connx


    # sql_query = """
    # SELECT d.[Calendar Year], d.[Calendar Month Number], sum(o.[Total Excluding Tax]) as [Total Order Amount]
    # FROM [Fact].[Order] as o JOIN [Dimension].[Date] as d ON o.[Order Date Key] = d.[Date]
    # GROUP BY d.[Calendar Year], d.[Calendar Month Number]
    # ORDER BY d.[Calendar Year], d.[Calendar Month Number]
    # """
    # df = pd.read_sql_query(sql_query, get_connx())
    # return json.dumps(df.to_dict(orient='records'))
    return """<Table><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>1</Calendar Month Number><Total Order Amount>3824842.85</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>2</Calendar Month Number><Total Order Amount>2821282.20</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>3</Calendar Month Number><Total Order Amount>3966078.10</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>4</Calendar Month Number><Total Order Amount>4155710.05</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>5</Calendar Month Number><Total Order Amount>4562830.35</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>6</Calendar Month Number><Total Order Amount>4150098.60</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>7</Calendar Month Number><Total Order Amount>4502741.85</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>8</Calendar Month Number><Total Order Amount>3601220.60</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>9</Calendar Month Number><Total Order Amount>3916003.25</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>10</Calendar Month Number><Total Order Amount>3879872.45</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>11</Calendar Month Number><Total Order Amount>3819809.10</Total Order Amount></Row><Row><Calendar Year>2013</Calendar Year><Calendar Month Number>12</Calendar Month Number><Total Order Amount>3728103.40</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>1</Calendar Month Number><Total Order Amount>4202578.80</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>2</Calendar Month Number><Total Order Amount>3572744.40</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>3</Calendar Month Number><Total Order Amount>3955257.55</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>4</Calendar Month Number><Total Order Amount>4212856.25</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>5</Calendar Month Number><Total Order Amount>4753224.10</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>6</Calendar Month Number><Total Order Amount>4427573.80</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>7</Calendar Month Number><Total Order Amount>4919791.85</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>8</Calendar Month Number><Total Order Amount>4197257.40</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>9</Calendar Month Number><Total Order Amount>3973877.85</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>10</Calendar Month Number><Total Order Amount>4606478.45</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>11</Calendar Month Number><Total Order Amount>4157270.55</Total Order Amount></Row><Row><Calendar Year>2014</Calendar Year><Calendar Month Number>12</Calendar Month Number><Total Order Amount>4513092.40</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>1</Calendar Month Number><Total Order Amount>4556065.25</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>2</Calendar Month Number><Total Order Amount>4307819.25</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>3</Calendar Month Number><Total Order Amount>4644642.35</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>4</Calendar Month Number><Total Order Amount>5222594.85</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>5</Calendar Month Number><Total Order Amount>4636628.45</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>6</Calendar Month Number><Total Order Amount>4696866.65</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>7</Calendar Month Number><Total Order Amount>5339212.00</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>8</Calendar Month Number><Total Order Amount>4070526.60</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>9</Calendar Month Number><Total Order Amount>4841896.70</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>10</Calendar Month Number><Total Order Amount>4653840.90</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>11</Calendar Month Number><Total Order Amount>4240612.30</Total Order Amount></Row><Row><Calendar Year>2015</Calendar Year><Calendar Month Number>12</Calendar Month Number><Total Order Amount>4607182.15</Total Order Amount></Row><Row><Calendar Year>2016</Calendar Year><Calendar Month Number>1</Calendar Month Number><Total Order Amount>4612140.45</Total Order Amount></Row><Row><Calendar Year>2016</Calendar Year><Calendar Month Number>2</Calendar Month Number><Total Order Amount>4099480.35</Total Order Amount></Row><Row><Calendar Year>2016</Calendar Year><Calendar Month Number>3</Calendar Month Number><Total Order Amount>4807110.70</Total Order Amount></Row><Row><Calendar Year>2016</Calendar Year><Calendar Month Number>4</Calendar Month Number><Total Order Amount>4739058.60</Total Order Amount></Row><Row><Calendar Year>2016</Calendar Year><Calendar Month Number>5</Calendar Month Number><Total Order Amount>5138002.65</Total Order Amount></Row></Table>"""

def sales_forecast(dataset)->str:
    sample_sales_forecast = """
[
  {"Year": 2016, "Month": 6, "Total Order Amount": 5345009.39},
  {"Year": 2016, "Month": 7, "Total Order Amount": 5209132.57},
  {"Year": 2016, "Month": 8, "Total Order Amount": 5217514.01}
]
    """
    return json.dumps(sample_sales_forecast)


def get_current_time(location):
    try:
        # Get the timezone for the city
        timezone = pytz.timezone(location)

        # Get the current time in the timezone
        now = datetime.now(timezone)
        current_time = now.strftime("%I:%M:%S %p")

        return current_time
    except:
        return "Sorry, I couldn't find the timezone for that location."


functions = [  
    {
        "name": "search_bing",
        "description": "1",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "retrieve_sales_report",
        "description": "Retrieves sales report from data warehouse that has sales data",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Sales report title and description",
                }
            },
            "required": ["query"],
        },
        "output":{
            "type": "object",
            "name": "sales report",
            "properties": {
                "dataset": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "Year": {
                            "type": "number",
                            "description": "The year of the sales data"
                        },
                        "Month": {
                            "type": "number",
                            "description": "The month of the sales data"
                        },
                        "Profits($M)": {
                            "type": "number",
                            "description": "The profits in millions for the given month and year"
                        }
                    },
                    "required": ["Year", "Month", "Profits($M)"],
                    "description": "An object representing sales data for a specific month and year"
                },
                "description": "The dataset for the sales"
            }
            },
        }
    },
    {
        "name": "sales_forecast",
        "description": "Makes a forecast on sales based on given dataset, if there is a sales report, use that as input, if there is no sales report, abort the forecast and return error",
        "parameters": {
        "type": "object",
        "properties": {
            "dataset": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "Year": {
                            "type": "number",
                            "description": "The year of the sales data"
                        },
                        "Month": {
                            "type": "number",
                            "description": "The month of the sales data"
                        },
                        "Profits($M)": {
                            "type": "number",
                            "description": "The profits in millions for the given month and year"
                        }
                    },
                    "required": ["Year", "Month", "Profits($M)"],
                    "description": "An object representing sales data for a specific month and year"
                },
                "description": "The dataset for the sales"
            }
        },
        "required": ["dataset"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get the current time in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name. The pytz is used to get the timezone for that location. Location names should be in a format like America/New_York, Asia/Bangkok, Europe/London",
                }
            },
            "required": ["location"],
        },
    },
    {
        "name": "pci_dss_v4",
        "description": "Searches the PCI DSS v4.0 document to get up to date information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "PCI DSS related search query",
                }
            },
            "required": ["query"],
        },
    },
]

available_functions = {
    "search_bing": search_bing,
    "retrieve_sales_report": retrieve_sales_report,
    "sales_forecast": sales_forecast,
    "get_current_time":get_current_time,
    "pci_dss_v4": pci_dss_v4
}

def run_multiturn_conversation(messages, functions, available_functions, deployment_name, verbose: bool=False):
    """
    Runs a multi-turn conversation with GPT4, where GPT4 may call functions
    :param messages: a list of messages in the conversation, where each message is a dict with keys "role" and "content"
    :param functions: a list of functions that GPT4 can call
    :param available_functions: a dict of function names to functions
    :param deployment_name: the name of the deployment to use


    """
    # Step 1: send the conversation and available functions to GPT

    response = openai.ChatCompletion.create(
        deployment_id=deployment_name,
        messages=messages,
        functions=functions,
        function_call="auto", 
        temperature=0
    )

    if verbose:
        print(response)

    # Step 2: check if GPT wanted to call a function
    while response["choices"][0]["finish_reason"] == 'function_call':
        if verbose:
            print("== Response Type: function_call {} ==".format(response["choices"][0]["finish_reason"]))
        
        response_message = response["choices"][0]["message"]
        
        if verbose:
            print("Recommended Function call:")
            print(response_message.get("function_call"))
            print()
        
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        
        function_name = response_message["function_call"]["name"]
        
        # verify function exists
        if function_name not in available_functions:
            return "Function " + function_name + " does not exist"
        function_to_call = available_functions[function_name]  
        
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)
        
        if verbose:
            print(function_name, "Output of function call:", function_response)
            print()
        
        # Step 4: send the info on the function call and function response to GPT
        
        # adding assistant response to messages
        messages.append(
            {
                "role": response_message["role"],
                "function_call": {
                    "name": response_message["function_call"]["name"],
                    "arguments": response_message["function_call"]["arguments"],
                },
                "content": None
            }
        )

        # adding function response to messages
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response

        if verbose:
            print("== Messages in next request:")
            for message in messages:
                print(message)
            print("=============================")

        response = openai.ChatCompletion.create(
            messages=messages,
            deployment_id=deployment_name,
            function_call="auto",
            functions=functions,
            temperature=0
        )  # get a new response from GPT where it can see the function response

        if verbose:
            print(response)

    return response, messages


def conversation(message, history):
    system_message = """You are an assistant designed to help business analyist and data analyist answer questions.
    You have access to query the web using Bing Search. You should call bing search whenever a question requires up to date information or could benefit from web data.
    You have access to data warehouse that has sales data. You should call retrieve_sales_report whenever a question requires historical sales data.
    You have access to a forecasting model that can make predictions on sales. You should call sales_forecast whenever a question requires sales forecast. Make sure to use output from retrieve_sales_report as input for sales_forecast.
    You have access to PCI DSS v4 document. You should call pci_dss_v4 whenever a question requires information from PCI DSS v4 document.

    In your answer, repeast the question and then call the appropriate function to get the answer.

    ## Safety

    If you don't have funtion or skill to answer a question, say you don't know. 

    ## Response

    If you used a Function Calling state that which function you used
    Reponse format
    [Funtion `function_name` called]

    [Your ansers]

    ### Example 1
    [Function `search_bing` called] 

    The latest price of Bitcoin is approximately $38,808.75 USD

    ### Example 2
    [Function `retrieve_sales_report` called]

    Latest date in the sales report is from May 2016. 

    """
        
    history_openai_format = []
    if len(history) == 0:        
        history_openai_format.append({"role": "system", "content": system_message})
    else: 
        history_openai_format.append({"role": "system", "content": system_message})
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})

    history_openai_format.append({"role": "user", "content": message})

    res, history_openai_format = run_multiturn_conversation(history_openai_format, functions, available_functions, ENGINE, verbose=False)
    return res.choices[0].message['content']
 
with gr.Blocks(fill_height=True) as app:
    gr.ChatInterface(conversation)

app.queue().launch()