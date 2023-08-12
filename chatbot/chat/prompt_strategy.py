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
        prompt_template = """Use the context to answer the question. Context and question are delimited by XML tags. If the context is not sufficient, say so and don't make up an answer.

        <context>
        {context}
        </context>

        <question>
        {question}
        </question>"""
        super().__init__(name="Strategy A", template=prompt_template,
                         input_variables=['context', 'question'])

    def generate_prompt(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.input_variables:
                raise KeyError

        return self.template.format(**kwargs)
