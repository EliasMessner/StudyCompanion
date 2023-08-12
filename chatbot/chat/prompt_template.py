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