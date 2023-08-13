from chat.prompt_strategies.retrieval_qa import RetrievalQA
from chat.prompt_strategies.standalone_question_qa import StandaloneQuestionConversationalRetrievalQA
from chat.prompt_strategies.summarized_conv_qa import SummarizedConversationPromptStrategy

# map string option from dropdown menu to strategy class instance
strategy_map = {
    'SummarizedConversationRetrievalQA': SummarizedConversationPromptStrategy(),
    'RetrievalQA': RetrievalQA(),
    'StandaloneQuestionConversationalRetrievalQA': StandaloneQuestionConversationalRetrievalQA()
}


class ChatController:
    def __init__(self):
        # set standard prompt strategy at the start
        self.prompt_strategy = RetrievalQA()

    def set_prompt_strategy(self, strat_str: str):
        print("Set prompt strategy to ", strat_str)
        self.prompt_strategy = strategy_map[strat_str]

    def set_language(self, language: str):
        self.prompt_strategy.set_language(language)

    def on_new_user_message(self, messages: list):
        return self.prompt_strategy.execute(messages=messages)
