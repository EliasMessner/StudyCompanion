from chat.prompt_templates.prompt_template import LanguagePromptTemplateFiller


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
