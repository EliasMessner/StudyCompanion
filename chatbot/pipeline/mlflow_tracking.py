import mlflow
import time

def log_ingestion(scraping_start_time, start_time, number_document_uploaded, keywords, number_scrape_uploaded):
    mlflow.set_experiment("group-7-track-uploads")
    with mlflow.start_run():
        mlflow.log_metric("ingestion time", scraping_start_time - start_time)
        mlflow.log_metric("number of uploaded documents", number_document_uploaded)
        mlflow.log_text(keywords, "keywords.txt")
        mlflow.log_metric("scraping time", time.time() - scraping_start_time)
        mlflow.log_metric("number of uploaded scraped documents", number_scrape_uploaded)
    return

def log_reply(start_time, user_message, message, model):
    mlflow.set_experiment("group-7-track-replies")
    with mlflow.start_run():
        mlflow.log_metric("response time", time.time() - start_time)
        i=0
        for score in message['scores']:
            mlflow.log_metric(f"response score {i}", score)
            i+=1
        mlflow.log_param("QA model", model)
        mlflow.log_text(str(user_message['content']), "user_message.txt")
        print(message['content'])
        mlflow.log_text(str(message['content']), "response.txt")
        mlflow.log_text(str(message['sources']), "sources.txt")
       