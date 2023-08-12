# abstract class (strategy design pattern), just create a new class for every new prompt strategy
from abc import ABC, abstractmethod

from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from chat.prompt_template import fill_simple_retrieval_QA_template
from pipeline.document_preprocessing import documents_to_unique_metadata, documents_to_linebreaked_strings
from pipeline.vectorstore_controller import VectorstoreController


class PromptStrategy(ABC):

    def __init__(self, input_variables) -> None:
        self.input_variables = input_variables
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

    def __init__(self) -> None:
        super().__init__(input_variables=['context', 'question'])

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