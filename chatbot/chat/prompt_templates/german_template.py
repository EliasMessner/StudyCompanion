from chat.prompt_templates.prompt_template import LanguagePromptTemplateFiller


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
