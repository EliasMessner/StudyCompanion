from trubrics.integrations.streamlit import FeedbackCollector
import os
from chat.prompt_strategies.prompt_strategy import PromptStrategy
from dotenv import load_dotenv
load_dotenv()


class FeedbackController:
    def __init__(self, prompt_strategy: PromptStrategy) -> None:
        self.prompt_strategy = prompt_strategy
        self.collector = FeedbackCollector(
            component_name="default",
            email=os.environ.get("TRUBRICS_EMAIL"),
            password=os.environ.get("TRUBRICS_PASSWORD"),
        )

    def load_st_component(self, key, prompt_question, prompt_answer, scores):
        metadata = {'question': prompt_question,
                    'answer': prompt_answer, 'scores': scores}
        # model name has to be something like prompt_strategy_a or prompt_strategy_b
        self.collector.st_feedback(feedback_type="thumbs", model=self.prompt_strategy.name,
                                   open_feedback_label="[Optional] Provide additional feedback", key=key, metadata=metadata)
