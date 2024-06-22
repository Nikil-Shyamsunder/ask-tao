from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_community.vectorstores import Qdrant
from langchain.document_loaders import DataFrameLoader
import pandas as pd

def add_human_prompt(content):
    messages.append(HumanMessage(content=content))

def get_response(prompt):
    # augment prompt
    augmented_prompt = custom_prompt(qdrant_tao, prompt)
    
    # process prompt
    add_human_prompt(augmented_prompt)
    
    # send to GPT
    res = chat.invoke(messages)

    # return response
    return res.content

def load_data():
    # Step 1: Read the text file
    file_path = 'tao-te-ching.txt'
    
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Step 2: Split the text into chunks
    def split_text_into_chunks(text, chunk_size=500):
        words = text.split()
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks
    
    chunks = split_text_into_chunks(text)
    
    # Step 3: Create a DataFrame
    data = {
        'chunk': chunks,
        'source': [file_path] * len(chunks)  # Assuming single file, modify if multiple sources
    }
    
    df = pd.DataFrame(data)
    
    # Step 4: Load the DataFrame as documents
    loader = DataFrameLoader(df, page_content_column="chunk")
    tao_documents = loader.load()

    # return documents 
    return tao_documents

def qdrant_client():
    tao_documents = load_data()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    api_key = ''
    url = 'http://localhost:6333'
    return Qdrant.from_documents(
        documents=tao_documents,
        embedding=embeddings,
        url=url,
        collection_name="tao_chatbot",
        api_key=api_key
        )

def custom_prompt(client, query: str):
    results = client.similarity_search(query, k=3)
    source_knowledge = "\n".join([x.page_content for x in results])
    print(source_knowledge)
    augment_prompt = f"""Using the contexts below, answer the query:

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augment_prompt

qdrant_tao = qdrant_client()

chat = ChatOpenAI(
    model='gpt-3.5-turbo'
)

messages = []


