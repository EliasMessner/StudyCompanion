import string

import nltk


def clean(text, stop_words):
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
