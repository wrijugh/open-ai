
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# for agents
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from dotenv import load_dotenv
import os

if load_dotenv("../.env"):
    print("Found OpenAPI Base Endpoint: " + os.getenv("OPENAI_API_BASE"))
else: 
    print("No file .env found")

openai_api_type = os.getenv("OPENAI_API_TYPE")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_version = os.getenv("OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME")
model_name = os.getenv("OPENAI_COMPLETION_MODEL") 
# embedding_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")



def langchain_agent():
    llm = AzureOpenAI(
        model_name = model_name,
        deployment_name = deployment_name,
        temperature = 0.7    
    )

    tool = load_tools(["wikipedia", "llm-math"], llm=llm)

    agent = initialize_agent(
        tool, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    result = agent.run("What is the average age od a dog? Multiply the age by 3.")

if __name__ == "__main__":
    # print(generate_pet_name("cow", "black"))
    print(langchain_agent())