import logging
import time
from pipeline.document_preprocessing import remove_short_paragraphs_from_documents, remove_short_documents, \
    split_documents
from pipeline.keyword_extraction_tfidf import get_keywords
from pipeline.pdf_and_text_utils import load_pdf
from pipeline.scraper import Scraper
from pipeline.vectorstore_controller import VectorstoreController
from pipeline.mlflow_tracking import log_ingestion

logging.basicConfig(level=logging.INFO)

class PipelineController:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        self.scraper = Scraper()
        self.vectorstore_controller = VectorstoreController()

    def ingest_pdf(self, path: str):
        start_time = time.time()
        documents = load_pdf(path)
        filtered_documents = remove_short_documents(documents, k_words=15)        
        number_document_uploaded = len(self.vectorstore_controller.add_documents_to_vectorstore(filtered_documents))

        keywords = get_keywords(documents)
        scraping_start_time = time.time()
        scraped_documents = self.scraper.scrape(keywords, n_per_site=5)
        filtered_documents = remove_short_paragraphs_from_documents(scraped_documents, paragraph_separator="\n\n", k_words=5)
        splitted_documents = split_documents(filtered_documents)
        number_scrape_uploaded = len(self.vectorstore_controller.add_documents_to_vectorstore(splitted_documents))
        log_ingestion(scraping_start_time, start_time, number_document_uploaded, keywords, number_scrape_uploaded)