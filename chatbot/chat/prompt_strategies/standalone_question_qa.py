from chat.prompt_strategies.prompt_strategy import PromptStrategy
import time
from pipeline.document_preprocessing import documents_to_unique_metadata, documents_to_linebreaked_strings
from pipeline.mlflow_tracking import log_reply


class StandaloneQuestionConversationalRetrievalQA(PromptStrategy):

    def execute(self, messages):
        start_time = time.time()
        chat_history = messages[1:-1]

        # generate new standalone question if there is a chat history
        if len(chat_history) > 0:
            # let llm generate first prompt (standalone question)
            first_prompt = self.language_prompt_template_filler.fill_standalone_question_generation_template(
                chat_history=chat_history, follow_up_question=messages[-1])
            print(first_prompt)

            # make request to llm with that first generated prompt
            response = self.chat_client.request(
                [{"role": "user", "content": first_prompt}])

            standalone_question = response['choices'][0]['message']['content']

        else:
            standalone_question = messages[-1]['content']

        # retrieve context and fill out standard prompt
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=standalone_question, k=3)
        documents = [document[0] for document in documents_with_scores]
        scores = [document[1] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        prompt = self.language_prompt_template_filler.fill_simple_retrieval_qa_template(
            context=documents_to_linebreaked_strings(documents), question=standalone_question)
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])

        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        log_reply(start_time, messages[-1], message,
                  "StandaloneQuestionConversationalRetrievalQA")
        return message
