"""Data Integration Pipeline. Loads pdf documents, stores their embeddings, and scrapes the web for keywords."""

import os

import pinecone
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Pinecone

load_dotenv()


class VectorStoreController:
    """
    Controller for writing to and querying from vectorstore.
    """

    def __init__(self) -> None:
        """Connects to the pinecone index (specified in .env)"""

        # connect to vectorstore
        index_name = os.getenv('PINECONE_INDEX_NAME')

        # initialize pinecone
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_API_ENV")
        )

        # load vectorstore and define embeddings to use later
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

    def add_documents_to_vectorstore(self, documents: list[Document]):
        """
        Creates embeddings from documents and stores them in the pinecone index.

        :param documents: The documents array to embed and store in the index
        :return: list of ids from adding the documents into the vectorstore.
        """
        return self.vectorstore.add_documents(documents)

    def add_text_to_vectorstore(self, text_split: list[str]):
        """
        Creates embeddings from a text and stores them in the pinecone index.

        :param text_split: The text_split array to embed and store in the index
        :return: list of ids from adding the texts into the vectorstore.
        """
        return self.vectorstore.add_texts(text_split)

    def query_vectorstore(self, query: str, k: int = 4, get_raw_text=False):
        """
        Performs similarity search in the pinecone index and returns the k most relevant documents.

        :param query: The query to search for in the pinecone index
        :param k: amount of documents to return
        :param get_raw_text: whether raw texts of the documents should be returned
        :return: k most relevant documents 
        """
        docs = self.vectorstore.similarity_search(query=query, k=k)
        print(docs)
        if get_raw_text:
            docs = [t.page_content for t in docs]

        return docs
