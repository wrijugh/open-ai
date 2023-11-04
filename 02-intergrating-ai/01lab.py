import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
if load_dotenv():
    print("Found OpenAI API Base Endpoint: " + os.getenv("OPENAI_API_BASE"))
else: 
    print("OpenAI API Base Endpoint not found. Have you configured the .env file?")
    
API_KEY = os.getenv("OPENAI_API_KEY")
# This version of the API is needed to properly retrieve the list of model deployments.
API_VERSION = "2023-03-15-preview"
RESOURCE_ENDPOINT = os.getenv("OPENAI_API_BASE")

url = RESOURCE_ENDPOINT + "/openai/deployments?api-version=" + API_VERSION

print (url)

r = requests.get(url, headers={"api-key": API_KEY})

print(r.text)