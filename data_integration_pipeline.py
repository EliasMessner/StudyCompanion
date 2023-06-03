from pdf_and_text_utils import load_pdf
from keyword_extraction_tfidf import get_search_terms, pdf_docs_to_str
from scraper import load_web_content
from vectorstore_controller import VectorstoreController


def process_pdf(pdf_path: str, vectorstore_controller: VectorstoreController):
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
