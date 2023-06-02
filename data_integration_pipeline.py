from langchain.document_loaders import PyPDFLoader, SeleniumURLLoader
from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import NLTKTextSplitter
import pinecone
import os
from dotenv import load_dotenv
from scraper import Scraper
from typing import List, Literal

load_dotenv()


def load_pdf(pdf_path: str):
    """
    :param pdf_path: file path of pdf to load
    :return: a list of documents, one element for each page
    """
    loader = PyPDFLoader(pdf_path)

    # load pages from pdf
    document_pages = loader.load()
    return document_pages


def load_web_content(browser: Literal["firefox", "chrome"] = "firefox", query: str = None):
    scraper = Scraper(browser=browser)

    medium_post_urls = scraper.get_medium_search_results(query=query)

    web_loader = SeleniumURLLoader(
        urls=medium_post_urls, browser=browser)
    web_content = web_loader.load()
    return web_content


def split_pdf(document_pages: List[Document]):
    """
    :param document_pages: document (as a list of pages) to split
    :return: a list of documents, one element for each split
    """
    # split texts to paragraphs
    text_splitter = NLTKTextSplitter(chunk_size=200, chunk_overlap=0)
    text_split = text_splitter.split_documents(document_pages)
    return text_split


def split_text_paragraphs(text: str):
    # Split text into paragraphs using double line breaks
    paragraphs = text.split('\n\n')
    return paragraphs


def split_document_paragraphs(document: Document) -> List[Document]:
    new_documents = []
    raw_text = document.page_content
    paragraphs = split_text_paragraphs(raw_text)

    for par in paragraphs:
        new_documents.append(
            Document(page_content=par, metadata=document.metadata))

    return new_documents


class DataIntegrationPipeline:
    """Data Integration Pipeline. Loads pdf documents, stores their embeddings, and scrapes the web for keywords."""

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
        self.docsearch = Pinecone.from_existing_index(
            index_name=index_name, embedding=embeddings)

    def add_documents_to_vectorstore(self, documents: List[Document]):
        """
        Creates embeddings from documents and stores them in the pinecone index.

        :param documents: The documents array to embed and store in the index
        :return: list of ids from adding the documents into the vectorstore.
        """
        return self.docsearch.add_documents(documents)

    def add_text_to_vectorstore(self, text_split: List[str]):
        """
        Creates embeddings from a text and stores them in the pinecone index.

        :param text_split: The text_split array to embed and store in the index
        :return: list of ids from adding the texts into the vectorstore.
        """
        return self.docsearch.add_texts(text_split)

    def query_vectorstore(self, query: str, k: int = 4, get_raw_text=False):
        """
        Performs similarity search in the pinecone index and returns the k most relevant documents.

        :param query: The query to search for in the pinecone index
        :param k: amount of documents to return
        :param get_raw_text: whether raw texts of the documents should be returned
        :return: k most relevant documents 
        """
        docs = self.docsearch.similarity_search(query=query, k=k)
        print(docs)
        if get_raw_text:
            docs = [t.page_content for t in docs]

        return docs
