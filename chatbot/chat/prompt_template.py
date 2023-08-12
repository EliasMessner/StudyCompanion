def fill_simple_retrieval_QA_template(context, question):
    return f"""
Use the context to answer the question. Context and question are delimited by XML tags. If the context is not sufficient, say so and don't make up an answer.

<context>
{context}
</context>

<question>
{question}
</question>
""" 

def fill_standalone_question_generation_template(chat_history, follow_up_question):
    chat_hist_str = str(chat_history)
    #chat_hist_str="[{'role': 'user', 'content': 'What is requirements engineering?'}, {'role':'assistant', 'content':'Requirements engineering is a process of gathering and defining what services should be provided by the system. It focuses on assessing if the system is useful to the business, discovering requirements, converting these requirements into some standard format, and checking that the requirements define the system that the customer wants.'}]"
    return f"""
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question that includes the given context of the conversation.
Chat History:
{chat_hist_str}
Follow Up Input:
{follow_up_question}
Your answer should follow the following format:
<Rephrased question here>
"""