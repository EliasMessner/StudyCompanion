import mlflow
import time

def log_ingestion(scraping_start_time, start_time, number_document_uploaded, keywords, number_scrape_uploaded):
    mlflow.set_experiment("group-7-track-uploads")
    with mlflow.start_run():
        mlflow.log_metric("ingestion time", scraping_start_time - start_time)
        mlflow.log_metric("number of uploaded documents", number_document_uploaded)
        mlflow.log_text("keywords", keywords)
        mlflow.log_metric("scraping time", time.time() - scraping_start_time)
        mlflow.log_metric("number of uploaded scraped documents", number_scrape_uploaded)
    return