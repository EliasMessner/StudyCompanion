from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import (LLMChain, RetrievalQA)
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from pipeline.vectorstore_controller import VectorstoreController
from pipeline.document_preprocessing import documents_to_linebreaked_strings, documents_to_unique_metadata


class PromptTemplate:
    def __init__(self, template, input_variables) -> None:
        self.template = template
        self.input_variables = input_variables

    def create_prompt(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.input_variables: 
                raise KeyError
        
        return self.template.format(**kwargs)

template = """Use the following pieces of context to answer the question at the end. If possible, try to incorporate every context piece. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}"""
basic_context_prompt_template = PromptTemplate(template=template, input_variables=["context", "question"])


class ChatController:
    def __init__(self):
        self.vectorstore_controller = VectorstoreController()
        self.chat_client = UniLeipzigChatClient()

    def on_new_user_message(self, messages: list):
        user_message = messages[-1]

        documents = self.vectorstore_controller.query_vectorstore(query=user_message['content'], k=3)
        sources = documents_to_unique_metadata(documents)
        prompt = basic_context_prompt_template.create_prompt(context=documents_to_linebreaked_strings(documents), question=user_message['content'])
        response = self.chat_client.request([{"role": "user", "content": prompt}])
        message = response['choices'][0]['message']
        message['sources'] = sources

        return message