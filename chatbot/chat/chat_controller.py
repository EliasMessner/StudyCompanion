from chat.prompt_strategy import PromptStrategyA


class ChatController:
    def __init__(self):
        self.prompt_strategy = PromptStrategyA()

    def on_new_user_message(self, messages: list):
        return self.prompt_strategy.execute(messages=messages)
