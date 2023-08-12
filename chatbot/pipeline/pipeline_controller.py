import logging

from pipeline.document_preprocessing import remove_short_paragraphs_from_documents, remove_short_documents, \
    split_documents
from pipeline.keyword_extraction_tfidf import get_keywords
from pipeline.pdf_and_text_utils import load_pdf
from pipeline.scraper import Scraper
from pipeline.vectorstore_controller import VectorstoreController

logging.basicConfig(level=logging.INFO)

class PipelineController:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        self.scraper = Scraper()
        self.vectorstore_controller = VectorstoreController()

    def ingest_pdf(self, path: str):
        documents = load_pdf(path)
        filtered_documents = remove_short_documents(documents, k_words=15)
        nonduplicate_documents = []
        for document in filtered_documents:
            if self.vectorstore_controller.query_vectorstore(document.page_content, k=1)[0][1]<0.99:
                nonduplicate_documents.append(document)
                print("duplicate detected")
        filtered_documents = nonduplicate_documents        
        self.vectorstore_controller.add_documents_to_vectorstore(filtered_documents)

        keywords = get_keywords(documents)
        scraped_documents = self.scraper.scrape(keywords, n_per_site=5)
        filtered_documents = remove_short_paragraphs_from_documents(scraped_documents, paragraph_separator="\n\n", k_words=5)
        splitted_documents = split_documents(filtered_documents)
        self.vectorstore_controller.add_documents_to_vectorstore(splitted_documents)