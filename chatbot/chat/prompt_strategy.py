# abstract class (strategy design pattern), just create a new class for every new prompt strategy
class PromptStrategy():
    def __init__(self, name: str, template, input_variables) -> None:
        self.input_variables = input_variables
        self.template = template
        self.name = name

    def generate_prompt(self, **kwargs):
        pass


class PromptStrategyA(PromptStrategy):
    """
    strategy, where the prompt does not hold any previous context
    """

    def __init__(self) -> None:
        prompt_template = """Use the following pieces of context to answer the question at the end. If possible, try to incorporate every context piece. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}"""
        super().__init__(name="Strategy A", template=prompt_template,
                         input_variables=['context', 'question'])

    def generate_prompt(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.input_variables:
                raise KeyError

        return self.template.format(**kwargs)
