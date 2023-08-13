from abc import ABC, abstractmethod


class LanguagePromptTemplateFiller(ABC):
    @abstractmethod
    def fill_simple_retrieval_qa_template(self, context: str, question: str):
        raise NotImplementedError

    @abstractmethod
    def fill_standalone_question_generation_template(self, chat_history, follow_up_question: str):
        raise NotImplementedError

    @abstractmethod
    def fill_summarization_template(self, chat_history, follow_up_question: str):
        raise NotImplementedError
