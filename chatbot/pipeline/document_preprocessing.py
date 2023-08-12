import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

LANGUAGES = ["english", "german"]


def documents_to_linebreaked_strings(documents: List[Document]):
    return "\n\n".join(document.page_content for document in documents)


def documents_to_unique_metadata(documents: List[Document]):
    metadata = [document.metadata for document in documents]
    unique_metadata = []
    for m in metadata:
        metadata_string = ""
        if "page" in m.keys():
            metadata_string = f"{m['source']} (Page {int(m['page'])})"
        else:
            metadata_string = m['source']
        unique_metadata.append(metadata_string)

    return list(set(unique_metadata))


def get_stopwords(languages=LANGUAGES):
    nltk.download('stopwords')
    nltk.download('punkt')
    return {sw for lang in languages for sw in nltk.corpus.stopwords.words(lang)}


def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    
    metadatas = [document.metadata for document in documents]
    texts = [document.page_content for document in documents]

    return text_splitter.create_documents(texts, metadatas)


def remove_short_paragraphs_from_documents(documents: List[Document], paragraph_separator: str, k_words: int) -> List[Document]:
    output = []
    for document in documents:
        text = document.page_content
        paragraphs = text.split(paragraph_separator)
        filtered_paragraphs = filter(lambda paragraph: len(paragraph.split(" ")) > k_words, paragraphs)

        document.page_content = paragraph_separator.join(filtered_paragraphs)
        output.append(document)

    return output


def remove_short_documents(documents: List[Document], k_words: int) -> List[Document]:
    filtered_documents = filter(lambda document: len(document.page_content.split(" ")) > k_words, documents)

    return list(filtered_documents)


def clean(documents: List[Document]) -> List[Document]:
    stopwords = get_stopwords()
 
    output = []
    for document in documents:
        text = document.page_content
        word_tokens = word_tokenize(text)
        word_tokens = [w for w in word_tokens if w not in string.punctuation]
        filtered = [w .lower() for w in word_tokens if not w.lower() in stopwords]

        filtered = []
        for word in word_tokens:
            if word not in stopwords:
                filtered.append(word)

        detokenized = TreebankWordDetokenizer().detokenize(filtered)
        document.page_content = detokenized
        output.append(document)
 
    return output
