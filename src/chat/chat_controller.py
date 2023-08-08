from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import (LLMChain, RetrievalQA)
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import pinecone
import os

from dotenv import load_dotenv
load_dotenv()

class ChatController:
    def __init__(self):
        index_name = os.getenv('PINECONE_INDEX_NAME')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_API_ENV")
        )

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

        llm = OpenAI()
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        self.retrievalQA = RetrievalQA.from_llm(llm=llm, retriever=retriever, return_source_documents=True)
        
        #retrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    def receive(self, text: str):
        result = self.retrievalQA({"query": text})

        return result