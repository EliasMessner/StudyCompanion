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


class EnglishPromptTemplateFiller(LanguagePromptTemplateFiller):

    def fill_simple_retrieval_qa_template(self, context, question):
        return f"""
Use the context to answer the question. Context and question are delimited by XML tags. If the context is not sufficient, say so and don't make up an answer.

<context>
{context}
</context>

<question>
{question}
</question>
"""

    def fill_standalone_question_generation_template(self, chat_history, follow_up_question):
        chat_hist_str = str(chat_history)
        return f"""
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question that includes the given context of the conversation.
Chat History:
{chat_hist_str}
Follow Up Input:
{follow_up_question}
Your answer should follow the following format:
<Rephrased question here>
"""

    def fill_summarization_template(self, chat_history, follow_up_question):
        return f"""
    Given the following conversation and a follow-up question, return a summary of the conversation history that\
    includes all relevant context to the question and rephrase the follow up question to be a standalone question.
    Chat History: {chat_history}
    Follow-Up Input: {follow_up_question}
    Your answer should follow the following format (replace only the text between the XML tags and keep the XML tags):
    \"\"\"
    Use the following pieces of context to answer the users question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    ----------------
    <context>
    *Relevant chat history excerpt as context here*
    </context>
    <question>
    *Rephrased question here*
    </question>
    \"\"\"
    """


class GermanPromptTemplateFiller(LanguagePromptTemplateFiller):

    def fill_simple_retrieval_qa_template(self, context, question):
        return f"""
Benutze den Kontext, um die Frage zu beantworten. Kontext und Frage sind durch XML-Tags getrennt. Wenn der Kontext nicht ausreicht, sage dies und erfinde keine Antwort.

<context>
{context}
</context>

<question>
{question}
</question>
"""

    def fill_standalone_question_generation_template(self, chat_history, follow_up_question):
        chat_hist_str = str(chat_history)
        return f"""
Formulieren Sie angesichts des folgenden Chatverlaufs und einer Folgefrage die Folgefrage so um, dass sie eine eigenständige Frage ist, die den gegebenen Kontext des Gesprächs einbezieht.
Chatverlauf:
{chat_hist_str}
Folgefrage:
{follow_up_question}
Ihre Antwort sollte dem folgenden Format folgen:
<umformulierte Frage>
"""

    def fill_summarization_template(self, chat_history, follow_up_question):
        return f"""
Gib angesichts des folgenden Chatverlaufs und einer Folgefrage eine Zusammenfassung des Konversationsverlaufs zurück, der 
den gesamten relevanten Kontext zur Frage enthält und formuliere die Folgefrage so um, dass sie eine eigenständige Frage ist.
Chat-Verlauf: {chat_history}
Follow-up-Eingabe: {follow_up_question}
Deine Antwort sollte dem folgenden Format folgen (ersetze nur den Text zwischen den XML-Tags und behalte die XML-Tags bei):
\"\"\"
Verwende die folgenden Kontextelemente, um die Frage des Benutzers zu beantworten.
Wenn du die Antwort nicht kennst, sag einfach, dass du es nicht weißt, und versuche nicht, eine Antwort zu erfinden.
----------------
<context>
*Relevanter Chat-Verlaufsauszug als Kontext hier*
</context>
<question>
*Frage hier umformuliert*
</question>
\"\"\"
"""


class LanguagePromptTemplateFactory():

    @staticmethod
    def create_language_prompt_template_filler(language: str) -> LanguagePromptTemplateFiller:
        if (language == "German"):
            return GermanPromptTemplateFiller()
        elif (language == "English"):
            return EnglishPromptTemplateFiller()
