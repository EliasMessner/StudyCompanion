from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document


def pdf_to_str(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return pdf_docs_to_str(documents)


def pdf_docs_to_str(pdf_docs: list[Document]):
    return ' '.join(doc.page_content for doc in pdf_docs)
