from pipeline.pdf_and_text_utils import load_pdf
from pipeline.keyword_extraction_tfidf import get_keywords
from pipeline.scraper import Scraper
from pipeline.vectorstore_controller import VectorstoreController
from pipeline.document_preprocessing import clean, remove_short_paragraphs_from_documents, remove_short_documents, split_documents
import logging

logging.basicConfig(level=logging.INFO)

class PipelineController:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        self.scraper = Scraper()
        self.vectorstore_controller = VectorstoreController()

    def ingest_pdf(self, path: str):
        documents = load_pdf(path)
        cleaned_documents = clean(documents)
        filtered_documents = remove_short_documents(cleaned_documents, k_words=15)
        self.vectorstore_controller.add_documents_to_vectorstore(filtered_documents)

        keywords = get_keywords(cleaned_documents)
        scraped_documents = self.scraper.scrape(keywords, n_per_site=5)
        filtered_documents = remove_short_paragraphs_from_documents(scraped_documents, paragraph_separator="\n\n", k_words=5)
        splitted_documents = split_documents(filtered_documents)
        cleaned_documents = clean(splitted_documents)
        self.vectorstore_controller.add_documents_to_vectorstore(cleaned_documents)