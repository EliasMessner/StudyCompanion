from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import NLTKTextSplitter

from keyword_extraction_tfidf import get_search_terms
from scraper import load_web_content
from vectorstore_controller import VectorStoreController


def process_pdf(pdf_path: str, vectorstore_controller: VectorStoreController):
    """
    load pdf and add to vector store
    extract keywords from pdf and scrape the web
    add scraped web content to vector store
    """
    # TODO add lines to notebook for demo
    pdf_docs = load_pdf(pdf_path)
    vectorstore_controller.add_documents_to_vectorstore(pdf_docs)
    pdf_str = pdf_docs_to_str(pdf_docs)
    search_query = get_search_terms(text=pdf_str)
    web_content = load_web_content('chrome', search_query)
    vectorstore_controller.add_documents_to_vectorstore(web_content)


def pdf_to_str(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return pdf_docs_to_str(documents)


def pdf_docs_to_str(pdf_docs: list[Document]):
    return ' '.join(doc.page_content for doc in pdf_docs)


def load_pdf(pdf_path: str):
    """
    :param pdf_path: file path of pdf to load
    :return: a list of documents, one element for each page
    """
    loader = PyPDFLoader(pdf_path)

    # load pages from pdf
    document_pages = loader.load()
    return document_pages


def split_pdf(document_pages: list[Document]):
    """
    :param document_pages: document (as a list of pages) to split
    :return: a list of documents, one element for each split
    """
    # split texts to paragraphs
    text_splitter = NLTKTextSplitter(chunk_size=200, chunk_overlap=0)
    text_split = text_splitter.split_documents(document_pages)
    return text_split


def split_document_paragraphs(document: Document) -> list[Document]:
    new_documents = []
    raw_text = document.page_content
    paragraphs = split_text_paragraphs(raw_text)

    for par in paragraphs:
        new_documents.append(
            Document(page_content=par, metadata=document.metadata))

    return new_documents


def split_text_paragraphs(text: str):
    # Split text into paragraphs using double line breaks
    paragraphs = text.split('\n\n')
    return paragraphs
