from abc import ABC, abstractmethod

from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from chat.prompt_template import fill_simple_retrieval_QA_template, fill_standalone_question_generation_template
from pipeline.document_preprocessing import documents_to_unique_metadata, documents_to_linebreaked_strings
from pipeline.vectorstore_controller import VectorstoreController


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
        user_message = messages[-1]
        # documents are a list of tuples (document, score)
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=user_message['content'], k=3)
        documents = [document[0] for document in documents_with_scores]
        scores = [document[1] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        prompt = fill_simple_retrieval_QA_template(
            context=documents_to_linebreaked_strings(documents), question=user_message['content'])
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])
        print(response)
        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        return message



class StandaloneQuestionConversationalRetrievalQA(PromptStrategy):
    
    def execute(self, messages):
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
        prompt = fill_simple_retrieval_QA_template(
            context=documents_to_linebreaked_strings(documents), question=standalone_question)
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])

        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        return message    