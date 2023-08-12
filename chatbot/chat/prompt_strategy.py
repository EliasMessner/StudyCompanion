from abc import ABC, abstractmethod
import time
from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from chat.prompt_template import fill_simple_retrieval_qa_template, fill_standalone_question_generation_template, fill_summarization_template
from pipeline.document_preprocessing import documents_to_unique_metadata, documents_to_linebreaked_strings
from pipeline.vectorstore_controller import VectorstoreController
from pipeline.mlflow_tracking import log_reply


class PromptStrategy(ABC):

    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.vectorstore_controller = VectorstoreController()
        self.chat_client = UniLeipzigChatClient()

    @abstractmethod
    def execute(self, messages):
        """
        Takes some input like context and question and returns the final message from the LLM to show the user.
        """
        raise NotImplementedError


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
        prompt = fill_simple_retrieval_qa_template(
            context=documents_to_linebreaked_strings(documents), question=user_message['content'])
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])
        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        log_reply(start_time, user_message, message, "RetrievalQA")
        return message



class StandaloneQuestionConversationalRetrievalQA(PromptStrategy):
    
    def execute(self, messages):
        start_time = time.time()
        chat_history = messages[1:-1]

        # generate new standalone question if there is a chat history
        if len(chat_history) > 0:
            # let llm generate first prompt (standalone question)
            first_prompt = fill_standalone_question_generation_template(chat_history=chat_history, follow_up_question=messages[-1])
            print(first_prompt)

            # make request to llm with that first generated prompt
            response = self.chat_client.request(
                [{"role": "user", "content": first_prompt}])

            standalone_question = response['choices'][0]['message']['content']
        else:
            standalone_question = messages[-1]['content']

        print("Standalone question: ", standalone_question)
        # retrieve context and fill out standard prompt
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=standalone_question, k=3)
        documents = [document[0] for document in documents_with_scores]
        scores = [document[1] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        prompt = fill_simple_retrieval_qa_template(
            context=documents_to_linebreaked_strings(documents), question=standalone_question)
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])

        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        log_reply(start_time, messages[-1], message, "StandaloneQuestionConversationalRetrievalQA")
        return message    


class SummarizedConversationPromptStrategy(PromptStrategy):
    """
    Strategy where the prompt contains a summary of the conversation.
    A first prompt is created, which is then sent to the chatbot, which then generates a second and final prompt.
    The final prompt contains the summary of the conversation and the follow-up question.
    """

    def execute(self, messages):
        start_time = time.time()
        follow_up_question = messages[-1]['content']
        chat_history = messages[:-1]
        # create first prompt from template
        first_prompt = fill_summarization_template(chat_history=chat_history[1:-1],
                                                   follow_up_question=follow_up_question)
        # send first prompt to chatbot to generate final prompt
        response = self.chat_client.request(
            [{"role": "user", "content": first_prompt}])
        final_prompt = response['choices'][0]['message']
        # get standalone question, i.e. the content between the <question> tags
        standalone_question = final_prompt['content'].split('<question>')[1].split('</question>')[0]
        # get the chat context, i.e. the content between the <context> tags
        chat_context = final_prompt['content'].split('<context>')[1].split('</context>')[0]
        # get knowledge context from vector store
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=standalone_question, k=3)
        documents = [document[0] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        scores = [document[1] for document in documents_with_scores]
        knowledge_context = documents_to_linebreaked_strings(documents)
        # create final prompt
        chat_context = f"<chat_context>\n{chat_context}\n</chat_context>" if chat_context else ""
        knowledge_context = f"<knowledge_context>\n{knowledge_context}\n</knowledge_context>" if knowledge_context else ""
        final_prompt = fill_simple_retrieval_qa_template(
            context=f"{chat_context}\n{knowledge_context}",
            question=standalone_question)
        print(final_prompt)
        final_response = self.chat_client.request(
            [{"role": "user", "content": final_prompt}])
        print(final_response)
        message = final_response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        log_reply(start_time, messages[-1], message, "SummarizedConversationPromptStrategy")
        return message