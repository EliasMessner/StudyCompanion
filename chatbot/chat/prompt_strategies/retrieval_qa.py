from chat.prompt_strategies.prompt_strategy import PromptStrategy
import time
from pipeline.document_preprocessing import documents_to_unique_metadata, documents_to_linebreaked_strings
from pipeline.mlflow_tracking import log_reply


class RetrievalQA(PromptStrategy):
    """
    strategy, where the prompt does not hold any previous context
    """

    def execute(self, messages):
        start_time = time.time()
        user_message = messages[-1]
        # documents are a list of tuples (document, score)
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=user_message['content'], k=3)
        documents = [document[0] for document in documents_with_scores]
        scores = [document[1] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        prompt = self.language_prompt_template_filler.fill_simple_retrieval_qa_template(
            context=documents_to_linebreaked_strings(documents), question=user_message['content'])
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])
        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        log_reply(start_time, user_message, message, "RetrievalQA")
        return message
