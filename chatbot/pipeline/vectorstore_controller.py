"""Data Integration Pipeline. Loads pdf documents, stores their embeddings, and scrapes the web for keywords."""

import os
import pinecone
import logging

from dotenv import load_dotenv
load_dotenv()

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Pinecone


class VectorstoreController:
    """
    Controller for writing to and querying from vectorstore.
    """

    def __init__(self) -> None:
        """Connects to the pinecone index (specified in .env)"""

        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Initializing pinecone connection in environment {os.getenv('PINECONE_API_ENV')} to index {os.getenv('PINECONE_INDEX_NAME')}")
        index_name = os.getenv('PINECONE_INDEX_NAME')
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_API_ENV")
        )

        # load vectorstore and define embeddings to use later
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

    def add_documents_to_vectorstore(self, documents: list[Document]):
        """
        Creates embeddings from documents and stores them in the pinecone index. It ensures that no duplicates are uploaded to the index.

        :param documents: The documents array to embed and store in the index
        :return: list of ids from adding the documents into the vectorstore.
        """
        no_duplicates_documents = []
        for document in documents:
            if self.query_vectorstore(document.page_content, k=1)[0][1]<0.99:
                no_duplicates_documents.append(document)
        added_documents = self.vectorstore.add_documents(no_duplicates_documents)
        self.logger.info(f"Added {len(added_documents)} documents to vector store")

        return added_documents

    def query_vectorstore(self, query: str, k: int = 4, get_raw_text=False):
        """
        Performs similarity search in the pinecone index and returns the k most relevant documents.

        :param query: The query to search for in the pinecone index
        :param k: amount of documents to return
        :param get_raw_text: whether raw texts of the documents should be returned
        :return: k most relevant documents with similarity score > 0.5
        """
        documents_with_scores = self.vectorstore.similarity_search_with_score(query=query, k=k)
        documents_with_scores = [document for document in documents_with_scores if document[1] > 0.5]
        if get_raw_text:
            documents_with_scores = [(document[0].page_content,document[1]) for document in documents]
        print(documents_with_scores)
        self.logger.info(f"Received {len(documents_with_scores)} documents from querying vectorstore")

        return documents_with_scores
