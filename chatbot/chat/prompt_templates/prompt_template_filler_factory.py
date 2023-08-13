from chat.prompt_templates.german_template import GermanPromptTemplateFiller
from chat.prompt_templates.english_template import EnglishPromptTemplateFiller
from chat.prompt_templates.prompt_template import LanguagePromptTemplateFiller


class LanguagePromptTemplateFactory():

    @staticmethod
    def create_language_prompt_template_filler(language: str) -> LanguagePromptTemplateFiller:
        if (language == "German"):
            return GermanPromptTemplateFiller()
        elif (language == "English"):
            return EnglishPromptTemplateFiller()
