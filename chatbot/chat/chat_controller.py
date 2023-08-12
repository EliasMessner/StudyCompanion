from chat.prompt_strategy import StandaloneQuestionConversationalRetrievalQA, SummarizedConversationPromptStrategy

class ChatController:
    def __init__(self):
        self.prompt_strategy = StandaloneQuestionConversationalRetrievalQA()

    def on_new_user_message(self, messages: list):
        return self.prompt_strategy.execute(messages=messages)
