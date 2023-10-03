import os
import json
import openai
import requests
import base64
from tqdm import tqdm
from dotenv import load_dotenv
from document_chunking import DocumentChunker
from azure.storage.blob import BlobServiceClient

BLOB_CONTAINER_NAME = "document-chunks"

load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

### Create Azure Search Vector-based Index
# Setup the Payloads header
headers = {'Content-Type': 'application/json','api-key': os.environ['AZURE_SEARCH_KEY']}
params = {'api-version': os.environ['AZURE_SEARCH_API_VERSION']}


def text_to_base64(text):
    # Convert text to bytes using UTF-8 encoding
    bytes_data = text.encode('utf-8')

    # Perform Base64 encoding
    base64_encoded = base64.b64encode(bytes_data)

    # Convert the result back to a UTF-8 string representation
    base64_text = base64_encoded.decode('utf-8')

    return base64_text

def create_index_azure_search(index_name: str="demo_index_0", isVector: bool=False):
    if isVector:
        index_payload = {
            "name": index_name,
            "fields": [
                {"name": "id", "type": "Edm.String", "key": "true", "filterable": "true" },
                {"name": "title","type": "Edm.String","searchable": "true","retrievable": "true"},
                {"name": "content","type": "Edm.String","searchable": "true","retrievable": "true"},
                {"name": "contentVector","type": "Collection(Edm.Single)","searchable": "true","retrievable": "true","dimensions": 1536,"vectorSearchConfiguration": "vectorConfig"},
                {"name": "name", "type": "Edm.String", "searchable": "true", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},
                {"name": "location", "type": "Edm.String", "searchable": "false", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},     
                {"name": "page_num","type": "Edm.Int32","searchable": "false","retrievable": "true"},
                # {"name": "keyphrases","type": "Collection(Edm.String)","searchable": "true","filterable": "false","retrievable": "true","sortable": "false","facetable": "false","key": "false","analyzer": "standard.lucene","synonymMaps": []}           
            ],
            "vectorSearch": {
                "algorithmConfigurations": [
                    {
                        "name": "vectorConfig",
                        "kind": "hnsw"
                    }
                ]
            },
            "semantic": {
                "configurations": [
                    {
                        "name": "my-semantic-config",
                        "prioritizedFields": {
                            "titleField": {
                                "fieldName": "title"
                            },
                            "prioritizedContentFields": [
                                {
                                    "fieldName": "content"
                                }
                            ],
                            "prioritizedKeywordsFields": []
                        }
                    }
                ]
            }
        }
    else:
        index_payload = {
            "name": index_name,
            "fields": [
                {"name": "id", "type": "Edm.String", "key": "true", "filterable": "true" },
                {"name": "title","type": "Edm.String","searchable": "true","retrievable": "true"},
                {"name": "content","type": "Edm.String","searchable": "true","retrievable": "true"},
                {"name": "name", "type": "Edm.String", "searchable": "true", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},
                {"name": "location", "type": "Edm.String", "searchable": "false", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},
                {"name": "page_num","type": "Edm.Int32","searchable": "false","retrievable": "true"},
                # {"name": "keyphrases","type": "Collection(Edm.String)","searchable": "true","filterable": "false","retrievable": "true","sortable": "false","facetable": "false","key": "false","analyzer": "standard.lucene","synonymMaps": []}           
            ],
            "semantic": {
                "configurations": [
                    {
                        "name": "my-semantic-config",
                        "prioritizedFields": {
                            "titleField": {
                                "fieldName": "title"
                            },
                            "prioritizedContentFields": [
                                {
                                    "fieldName": "content"
                                }
                            ],
                            "prioritizedKeywordsFields": []
                        }
                    }
                ]
            }
        }

    r = requests.put(os.environ['AZURE_SEARCH_ENDPOINT'] + "/indexes/" + index_name, data=json.dumps(index_payload), headers=headers, params=params)
    print(r.status_code)
    print(r.ok)    
 

def upload_index_azure_search(index_name: str="demo_index_0", isVector: bool=False):
    print("Upload data to index")
    if isVector:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("CONNECTION_STRING"))
        # get a list of blobs using blob_service_client
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        blob_list = container_client.list_blobs()
        # read data in the blob
        for blob in blob_list:
            blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=blob.name)
            # print(blob_client.url)
            #https://openaiembedding.blob.core.windows.net/chunck-txt/Preferred_Gold_EPO_1500_Benefit_2022_in_Washington_0.txt
            # get file name for the blob.url to use it as document_name
            document_name = blob.name.split("/")[-1].split(".")[0]        
            page_num = int(document_name.split("_")[-1]) + 1
            blob_data = blob_client.download_blob().readall()
            blob_data = blob_data.decode("utf-8", "ignore")
            title = blob_data.split("\n")[0].replace("\n", "").replace("\r", "")
            try:
                upload_payload = {
                    "value": [
                        {
                            "id": text_to_base64(document_name),
                            "title": f"{title}",
                            "content": blob_data,
                            "contentVector": openai.Embedding.create(input=[blob_data], engine="text-embedding-ada-002")["data"][0]["embedding"],
                            "name": document_name,
                            "location": blob_client.url,
                            "page_num": page_num,
                            "@search.action": "upload"
                        },
                    ]
                }
                
                r = requests.post(os.environ['AZURE_SEARCH_ENDPOINT'] + "/indexes/" + index_name + "/docs/index", data=json.dumps(upload_payload), headers=headers, params=params)
                print(r.status_code)
                print(r.text)
            except Exception as e:
                print("Exception:",e)
                # print(content)
                continue

    else:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("CONNECTION_STRING"))
        # get a list of blobs using blob_service_client
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        blob_list = container_client.list_blobs()
        # read data in the blob
        for blob in blob_list:
            blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=blob.name)
            #https://openaiembedding.blob.core.windows.net/chunck-txt/Preferred_Gold_EPO_1500_Benefit_2022_in_Washington_0.txt
            # get file name for the blob.url to use it as document_name
            document_name = blob.name.split("/")[-1].split(".")[0]        
            page_num = int(document_name.split("_")[-1]) + 1
            blob_data = blob_client.download_blob().readall()
            blob_data = blob_data.decode("utf-8", "ignore")
            title = blob_data.split("\n")[0].replace("\n", "").replace("\r", "")
            try:
                upload_payload = {
                    "value": [
                        {
                            "id": text_to_base64(document_name),
                            "title": f"{title}",
                            "content": blob_data,
                            "name": document_name,
                            "location": blob_client.url,
                            "page_num": page_num,
                            "@search.action": "upload"
                        },
                    ]
                }
                
                r = requests.post(os.environ['AZURE_SEARCH_ENDPOINT'] + "/indexes/" + index_name + "/docs/index", data=json.dumps(upload_payload), headers=headers, params=params)
                if r.status_code != 200:
                    print(r.status_code)
                    print(r.text)
            except Exception as e:
                print("Exception:",e)
                # print(content)
                continue


if __name__ == "__main__":
    document_chuncks = DocumentChunker()
    # document_chuncks.run()
    create_index_azure_search()
    upload_index_azure_search()

    index_name = "demo_index_vector"
    create_index_azure_search(index_name, isVector=True)
    upload_index_azure_search(index_name, isVector=True)       

