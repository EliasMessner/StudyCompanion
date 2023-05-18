import string

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer


def get_top_n_keywords(text, n, stop_words=None):
    if stop_words is None:
        stop_words = get_stopwords("english", "german")
    tokens = preprocess_text(text, stop_words)
    kw_scores = get_keyword_scores(tokens)
    return [item[0] for item in sorted(kw_scores.items(), key=lambda item: item[1], reverse=True)][:n]


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


def get_keyword_scores(tokens):
    """
    Returns a dict mapping each unique token to its TF-IDF score
    """
    # Join tokens back into a string
    text = ' '.join(tokens)
    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    # Compute TF-IDF scores
    tfidf_matrix = vectorizer.fit_transform([text])
    # Get the feature names (tokens)
    feature_names = vectorizer.get_feature_names_out()
    # Create a dictionary of token to TF-IDF score
    keyword_scores = {}
    for col in tfidf_matrix.nonzero()[1]:
        keyword_scores[feature_names[col]] = tfidf_matrix[0, col]
    return keyword_scores
