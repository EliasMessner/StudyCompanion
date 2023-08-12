from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import (LLMChain, RetrievalQA)
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from chat.uni_leipzig_chat_client import UniLeipzigChatClient
from pipeline.vectorstore_controller import VectorstoreController
from pipeline.document_preprocessing import documents_to_linebreaked_strings, documents_to_unique_metadata
from chat.prompt_strategy import PromptStrategy


class ChatController:
    def __init__(self, prompt_strategy: PromptStrategy):
        self.prompt_strategy = prompt_strategy
        self.vectorstore_controller = VectorstoreController()
        self.chat_client = UniLeipzigChatClient()

    def on_new_user_message(self, messages: list):
        user_message = messages[-1]
        #documents are a list of tuples (document, score)
        documents_with_scores = self.vectorstore_controller.query_vectorstore(
            query=user_message['content'], k=3)
        documents= [document[0] for document in documents_with_scores]
        sources = documents_to_unique_metadata(documents)
        prompt = self.prompt_strategy.generate_prompt(
            context=documents_to_linebreaked_strings(documents), question=user_message['content'])
        print(prompt)
        response = self.chat_client.request(
            [{"role": "user", "content": prompt}])
        message = response['choices'][0]['message']
        message['sources'] = sources

        return message
