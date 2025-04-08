import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
# from indexer import Indexer

load_dotenv(dotenv_path="./.env",override=True)
endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')
key = os.getenv('AZURE_FORM_RECOGNIZER_KEY')


def get_document_analysis(filename):
    # sample document
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(filename, "rb") as f:
        print("Analyzing {}".format(filename))
        poller = document_analysis_client.begin_analyze_document("prebuilt-layout",f)
        result = poller.result()
        print("Analysis completed.")
        # save result as json

    return result

def parse_document(filename):
    """
    1. Extract text and table from a document using Azure Document Intelligence AI
    2. Return a list that has result as text file with text and table in each page
    """
    result = get_document_analysis(filename)
    doc_pages = []

    print("Extracting text and table from document...")
    for page in result.pages:
        # extract text from page
        markdown_table = ""
        text = ""

        for line in page.lines:
            text += line.content + " "

        # extract table from page
        for table_idx, table in enumerate(result.tables):
            for bounding_region_idx, bounding_region in enumerate(table.bounding_regions):
                # check page number
                if bounding_region.page_number == page.page_number:
                    markdown_table = ""
                    
                    data = table.cells
                    # Convert data to 2D list
                    table = [["" for _ in range(max(cell.column_index for cell in data) + 1)] for _ in range(max(cell.row_index for cell in data) + 1)]  
                    for cell in data:  
                        table[cell.row_index][cell.column_index] = cell.content  
                    
                    # Convert 2D list to markdown  
                    markdown_table = ["| " + " | ".join(row) + " |" for row in table]  
                    header_seperator = ["|---" * len(table[0]) + "|"]  
                    markdown_table = markdown_table[:1] + header_seperator + markdown_table[1:]  
                    
                    markdown_table = "\n".join(markdown_table)

        # add text and markdown table
        doc_pages.append({
            "page_number": page.page_number,
            "text": text,
            "markdown_table": markdown_table
        })
    return doc_pages

def save_parsed_document(doc_pages, source_filename: str="source_document", target_folder: str="data/chunking"):
    print("Saving parsed document to {}...".format(target_folder))
    # check folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # save doc_pages as text per item in list
    for page in doc_pages: # {str(i).zfill(2)}
        with open(os.path.join(target_folder,"{}-{}.txt".format(source_filename, str(page["page_number"]).zfill(4))), "w") as f:
            print("saving file {} {}-{}.txt".format(target_folder, source_filename, str(page["page_number"]).zfill(4)))
            f.write(page["text"]+"\n"+page["markdown_table"])
    

# upload files to blob container
def upload_blob(source_folder, target_container):
    print("Uploading files to blob container...")
    uploaded_files = []
    # Create a BlobServiceClient object by passing the connection string  
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("CONNECTION_STRING"))
    
    try:  
        container_client = blob_service_client.create_container(target_container)  
        print(f"Container {target_container} created.")  
    except ResourceExistsError as e:
        print(f"Container {target_container} already exists.")
        container_client = blob_service_client.get_container_client(target_container)  
    
    file_list = os.listdir(source_folder)
    # get file path
    file_path = [os.path.join(source_folder, file) for file in file_list]
    # loop through file path
    for path in file_path:
        blob_client = blob_service_client.get_blob_client(
            container=target_container, blob=os.path.basename(path))
        
        with open(path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, encoding="utf-8")
            uploaded_files.append(blob_client.url)   
            print(f"File {path} uploaded to {target_container} container.")

# main function
if __name__ == "__main__":
    print("starting...")
    # get current file location
    current_dir = os.path.dirname(__file__)
    filename = os.path.join("data", "FILE_NAME")
    target_folder = os.path.join(current_dir, "data","doc","chunking")
    blob_container_name = "doc"
    source_file_full_path = os.path.join(current_dir, filename)
    idx_name = "doc-idx"

    print("Running code in {} folder".format(current_dir))
    print("Parsing document {}".format(source_file_full_path))
    print("Saving parsed document to {}".format(target_folder))

    if os.path.exists(source_file_full_path):
        raise Exception("{} file does not exist.".format(source_file_full_path))

    save_parsed_document(
        parse_document(source_file_full_path), 
        source_filename=os.path.basename(source_file_full_path).split(".")[0],
        target_folder=target_folder)

    # Optional step to build index of each page for later use
    # upload_blob(os.path.join(current_dir,target_folder), blob_container_name)
    # indexer = Indexer(blob_conatiner_name=blob_container_name, index_name=idx_name, isVector=True)
    # indexer.run()
