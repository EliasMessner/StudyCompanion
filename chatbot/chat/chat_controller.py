from chat.prompt_strategy import RetrievalQA


class ChatController:
    def __init__(self):
        self.prompt_strategy = RetrievalQA()

    def on_new_user_message(self, messages: list):
        return self.prompt_strategy.execute(messages=messages)
