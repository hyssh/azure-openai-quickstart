import os
import dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError
from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

dotenv.load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def doxc2txt(filepath):
    print("Start to load docx file")
    loader = Docx2txtLoader(filepath)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 700,
        chunk_overlap  = 35,
        length_function = len,
    )

    texts = text_splitter.split_documents(data)

    i = 0 
    prefixfilename  = os.path.splitext(os.path.basename(filepath))[0]
    for t in texts:
        # save text as txt file
        with open(f"./chunks-txt/{prefixfilename}_{texts.index(t)}.txt", "w") as f:
            f.write(t.page_content)


def pdf2txt(filepath, extract_page: bool=True):
    print("Start to load pdf file")
    loader = PyPDFLoader(filepath)
    data = loader.load()

    if extract_page:
        prefixfilename  = os.path.splitext(os.path.basename(filepath))[0]
        for i in range(0, len(data)):
            with open(f"./chunks-txt/{prefixfilename}_{str(data[i].metadata['page'])}.txt", "w") as f:
                f.write(data[i].page_content)
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 700,
            chunk_overlap  = 35,
            length_function = len,
        )

        texts = text_splitter.split_documents(data)

        i = 0 
        prefixfilename  = os.path.splitext(os.path.basename(filepath))[0]
        for t in texts:
            # save text as txt file
            with open(f"./chunks-txt/{prefixfilename}_{texts.index(t)}.txt", "w") as f:
                f.write(t.page_content)



# upload files to blob container
def upload_blob(source_folder, target_container):
    # Create a BlobServiceClient object by passing the connection string  
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    
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
            blob_client.upload_blob(data, overwrite=True)        
            print(f"File {path} uploaded to {target_container} container.")

if __name__ == "__main__":
    print("Check folders")
    # cehck folder exist
    if not os.path.exists("./chunks-txt"):
        os.makedirs("./chunks-txt")

    if not os.path.exists("./data"):
        print("Can't find data folder. Please create a data folder and put your files in it.")
        exit()

    # get file list from folder
    file_list = os.listdir("./data")
    # get file path
    file_path = [os.path.join("./data", file) for file in file_list]
    # loop through file path
    for path in file_path:
        # check if file is docx
        if path.endswith(".docx"):
            # run docx2txt function
            doxc2txt(path)
            # upload_blob("./chunks-txt", "docx-chunk")
        elif path.endswith(".pdf"):
            pdf2txt(path)
            # upload_blob("./chunks-txt", "pdf-chunk")
        else:
            print("File format not supported.")
            continue
    
    