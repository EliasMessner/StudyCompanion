import string

import nltk


def clean_text(text, stop_words):
    """
    preprocess given text and concatenate resulting tokens
    :param text: text to clean
    :param stop_words: stop words ignore
    :return: cleaned text as one string
    """
    return ' '.join(preprocess_text(text, stop_words))


def get_stopwords(*languages):
    return [sw for lang in languages for sw in nltk.corpus.stopwords.words(lang)]


def preprocess_text(text, stop_words):
    # tokenize
    tokens = nltk.tokenize.word_tokenize(text)
    # remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    # remove stopwords and make lowercase
    tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
    return tokens
