# abstract class (strategy design pattern), just create a new class for every new prompt strategy
from abc import ABC, abstractmethod

from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from pipeline.document_preprocessing import documents_to_unique_metadata, documents_to_linebreaked_strings
from pipeline.vectorstore_controller import VectorstoreController


class PromptStrategy(ABC):

    def __init__(self, input_variables) -> None:
        self.input_variables = input_variables
        self.name = self.__class__.__name__
        self.vectorstore_controller = VectorstoreController()
        self.chat_client = UniLeipzigChatClient()

    def generate_prompt(self, template, **kwargs):
        for key, value in kwargs.items():
            if key not in self.input_variables:
                raise KeyError

        return template.format(**kwargs)

    @abstractmethod
    def execute(self, **kwargs):
        """
        Takes some input like context and question and returns the final message from the LLM to show the user.
        """
        raise NotImplementedError


class PromptStrategyA(PromptStrategy):
    """
    strategy, where the prompt does not hold any previous context
    """

    def __init__(self) -> None:
        super().__init__(input_variables=['context', 'question'])

    def execute(self, **kwargs):
        final_prompt_template = """Use the context to answer the question. Context and question are delimited by XML tags. If the context is not sufficient, say so and don't make up an answer.

                <context>
                {context}
                </context>

                <question>
                {question}
                </question>"""

        user_message = kwargs["messages"][-1]
        # documents are a list of tuples (document, score)
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=user_message['content'], k=3)
        documents = [document[0] for document in documents_with_scores]
        scores = [document[1] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        prompt = self.generate_prompt(
            template=final_prompt_template,
            context=documents_to_linebreaked_strings(documents), question=user_message['content'])
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])
        print(response)
        message = response['choices'][0]['message']
        message['sources'] = sources
        message['scores'] = scores
        return message


class SummarizedConversationPromptStrategy(PromptStrategy):
    """
    Strategy where the prompt contains a summary of the conversation.
    A first prompt is generated, which is then sent to the chatbot, which then generates a second and final prompt.
    The final prompt contains the summary of the conversation and the follow-up question.
    """

    def __init__(self) -> None:
        self.first_prompt_template = \
            """\
            Given the following conversation and a follow up question, return the conversation history excerpt that\
            includes any relevant context to the question if it exists and rephrase the follow-up question to be a\
            standalone question.
            Chat History: {chat_history}
            Follow Up Input: {follow_up_input}
            Your answer should follow the following format (replace only the text between the XML tags and keep the tags):
            \"\"\"
            Use the following pieces of context to answer the users question.\
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            ----------------
            <context>
            *Relevant chat history excerpt as context here*
            </context>
            <question>
            *Rephrased question here*
            </question>
            \"\"\"
            """
        super().__init__(input_variables=['chat_history', 'follow_up_input'])

    def generate_final_prompt(self, **kwargs):
        first_prompt = self.generate_prompt(**kwargs)
        chat_client = UniLeipzigChatClient()
        response = chat_client.request(messages=[first_prompt])
        second_prompt = response['choices'][0]['message']
        return second_prompt

