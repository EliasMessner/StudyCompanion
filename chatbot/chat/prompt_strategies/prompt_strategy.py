from abc import ABC, abstractmethod
from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from pipeline.vectorstore_controller import VectorstoreController
from chat.prompt_templates.prompt_template_filler_factory import LanguagePromptTemplateFactory


class PromptStrategy(ABC):

    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.vectorstore_controller = VectorstoreController()
        self.chat_client = UniLeipzigChatClient()

        # set standard prompt language to English
        self.language = 'English'
        self.language_prompt_template_filler = LanguagePromptTemplateFactory.create_language_prompt_template_filler(
            self.language)

    def set_language(self, language: str):
        self.language = language
        self.language_prompt_template_filler = LanguagePromptTemplateFactory.create_language_prompt_template_filler(
            self.language)

    @abstractmethod
    def execute(self, messages):
        """
        Takes some input like context and question and returns the final message from the LLM to show the user.
        """
        raise NotImplementedError
