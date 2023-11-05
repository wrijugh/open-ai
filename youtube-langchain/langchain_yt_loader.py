from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Faiss Library for vector search
from langchain.vectorstores import FAISS 

from dotenv import load_dotenv
import os

# load_dotenv("../.env")
if load_dotenv(dotenv_path= ".env"):
    print("Found OpenAPI Base Endpoint: " + os.getenv("OPENAI_API_BASE"))
else: 
    print("No file .env found")

openai_api_type = os.getenv("OPENAI_API_TYPE")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_api_version = os.getenv("OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME")
model_name = os.getenv("OPENAI_COMPLETION_MODEL") 
embedding_deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
embedding_model_name = os.getenv("OPENAI_EMBEDDING_MODEL")

# print(model_name, deployment_name)

# embaddings = OpenAIEmbeddings()
embeddings_model = OpenAIEmbeddings(
    openai_api_type = openai_api_type,
    openai_api_version = openai_api_version,
    openai_api_base = openai_api_base,
    openai_api_key = openai_api_key,
    deployment_name = embedding_deployment_name,
    model_name=embedding_model_name,
    chunk_size = 1
)

# video_url = "https://www.youtube.com/watch?v=-QH8fRhqFHM"
def create_vector_db_from_youtube_url(video_url) -> FAISS:
    # Load the youtube video
    youtube_loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = youtube_loader.load()
    # print(transcript)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    docs = text_splitter.split_documents(transcript)
    # print(docs)
    # pip install faiss-gpu
    db = FAISS.from_documents(docs, embeddings_model)
    
    return db


def get_response_from_query(db, query, k=2):
    docs = db.similarity_search(query=query, k=k)
    docs_page_content = " ".join([doc.page_content for doc in docs])
    
    llm = AzureChatOpenAI(
        openai_api_type = openai_api_type,
        openai_api_version = openai_api_version,
        openai_api_base = openai_api_base,
        openai_api_key = openai_api_key,
        model_name = model_name,
        deployment_name = deployment_name,
        temperature = 0
    )   
    # """
    #         You are helpful YouTube assistant that can answer questions about 
    #         videos based on the video's transcript.

    #         Answe the following question about the video: {question}
    #         By searching the following video transcript: {docs}

    #         Only use the factual information from the transcript to answer the question.

    #         If you feel like you don't have enough information to answer the question, 
    #         say "I don't know".

    #         Your answer should be detailed.
    #         """
    prompt_template = PromptTemplate(
        input_variables=["question", "docs"],
        # input_variables=["question"],
        template="""
            Find answer to the question: {question}. The answer should be from {docs}. 
            Please elaborate your answer.
            
            """
    )
        
    chain = LLMChain(llm=llm, prompt=prompt_template, output_key="answer")
    response = chain.run({ "question": query, "docs": docs_page_content })

    response = response.replace("\n", "###")
    # response = "Nothing test."
    return response
        

