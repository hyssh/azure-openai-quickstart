import os
import dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

dotenv.load_dotenv()

class DocumentChunker:
    def __init__(self, data_source_path: str='./data', chunk_target_path: str='./chunks-txt', container_name: str='document-chunks'):
        self.data_source_path = data_source_path
        self.chunk_target_path = chunk_target_path
        self.container_name = container_name

    def doxc2txt(self, filepath):
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
            with open(f"./{self.chunk_target_path}/{prefixfilename}_{texts.index(t)}.txt", "w") as f:
                f.write(t.page_content)


    def pdf2txt(self, filepath, extract_page: bool=True):
        loader = PyPDFLoader(filepath)
        data = loader.load()

        if extract_page:
            prefixfilename  = os.path.splitext(os.path.basename(filepath))[0]
            for i in range(0, len(data)):
                with open(f"./{self.chunk_target_path}/{prefixfilename}_{str(data[i].metadata['page'])}.txt", "w") as f:
                    f.write(data[i].page_content)
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap  = 100,
                length_function = len,
            )

            texts = text_splitter.split_documents(data)

            i = 0 
            prefixfilename  = os.path.splitext(os.path.basename(filepath))[0]
            for t in texts:
                # save text as txt file
                with open(f"./{self.chunk_target_path}/{prefixfilename}_{texts.index(t)}.txt", "w") as f:
                    f.write(t.page_content)


    # upload files to blob container
    def upload_blob(self, source_folder, target_container):
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
        return uploaded_files

    def run(self):
        print("Check folders")
        # check folder exist
        if not os.path.exists(self.chunk_target_path):
            os.makedirs(self.chunk_target_path)

        if not os.path.exists(self.data_source_path):
            print("Can't find data folder. Please create a data folder and put your files in it.")
            exit()

        # get file list from folder
        file_list = os.listdir(self.data_source_path)
        # get file path
        file_path = [os.path.join(self.data_source_path, file) for file in file_list]
        # loop through file path
        for path in file_path:
            print(path)
            # check if file is docx
            if path.endswith(".docx"):
                self.doxc2txt(path)
            elif path.endswith(".pdf"):
                self.pdf2txt(path)
            else:
                print(f"{path} not supported.")
                None
        self.upload_blob(self.chunk_target_path, self.container_name)
        
    
    