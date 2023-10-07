import os
import openai
import dotenv
import pandas as pd
from IPython.display import display, Markdown

dotenv.load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

ENGINE = "chat-gpt"
TEMPERATURE = 0.1
MAX_TOKENS = 2000
TOP_P = 1
FREQUENCY_PENALTY = 0.0
PRESENCE_PENALTY = 0.0

