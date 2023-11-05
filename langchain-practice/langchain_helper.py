
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
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


def generate_pet_name(animal_type, pet_color):
    
    llm = AzureOpenAI(
        model_name = model_name,
        deployment_name = deployment_name,
        temperature = 0.7    
    )

    prompt_template_name = PromptTemplate(
        input_variables=['animal_type', 'pet_color'],
        template="I have a {animal_type} and I want a cool name for it. It is {pet_color} in color. Suggest five cool names for it."
    )

    # name_chain = LLMChain(llm=llm, prompt=prompt_template_name)
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="pet_name")

    response = name_chain(
        {
            "animal_type": animal_type,
            "pet_color": pet_color
        }
    )

    return response

if __name__ == "__main__":
    print(generate_pet_name("cow", "black"))