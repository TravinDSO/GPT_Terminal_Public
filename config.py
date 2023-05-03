import os
from dotenv import load_dotenv

load_dotenv('enviroment.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Model costs: https://openai.com/pricing

# OpenAI API Completion Model rewrite_text function
# https://platform.openai.com/docs/models
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions" #default
OPENAI_API_MODEL = "gpt-3.5-turbo" #default
#OPENAI_API_ENDPOINT = "https://api.openai.com/v1/completions" #cheaper cost for testing
#OPENAI_API_MODEL = "text-ada-001" #cheaper cost for testing

# OpenAI API Embeddings Model process_question function
# https://platform.openai.com/docs/models/embeddings
EMBEDDINGS_MODEL = "text-embedding-ada-002" #Do not change as this is the best and cheapest model used for embeddings

# Langchain Model that processes indexed data
LANGCHAIN_MODEL = "text-davinci-003" #default
#LANGCHAIN_MODEL = "text-ada-001" #cheaper cost for testing | can also use "text-babbage-001"