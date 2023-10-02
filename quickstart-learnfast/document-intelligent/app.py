"""
This code sample shows Prebuilt Layout operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs
https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/quickstarts/try-v3-python-sdk
"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""

load_dotenv()
endpoint = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT')
key = os.getenv('AZURE_FORM_RECOGNIZER_KEY')

# sample document
formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
    
# poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-layout", formUrl)
filepath = "./data/Preferred_Gold_EPO_1500_Benefit_2023_in_Washington.pdf"
filepath = "C:/Users/hyssh/workspace/openai-demo/quickstart-learnfast/document-intelligent/data/Preferred_Gold_EPO_1500_Benefit_2023_in_Washington.pdf"
with open(filepath, "rb") as f:
    poller = document_analysis_client.begin_analyze_document("prebuilt-layout",f )
    result = poller.result()


# for para_index, paragraph in enumerate(result.paragraphs):
#     if paragraph.role == "pageNumber":
#         if hasattr(paragraph, "bounding_regions") and len(paragraph.bounding_regions) > 0:
#             print(f"Book page {paragraph.content} is found on pdf page {paragraph.bounding_regions[0].page_number}")
#         else:
#             print(f"Book page {paragraph.content} is not found on any pdf page")
#     else:
#         pass

for table_idx, table in enumerate(result.tables):
    print("--- Table No. {} ---".format(table_idx + 1))
    print(
        "Table # {} has {} rows and {} columns".format(
        table_idx, table.row_count, table.column_count
        )
    )
        
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
            cell.row_index,
            cell.column_index,
            cell.content.encode("utf-8"),
            )
        )

    print("--- Table End ---")
