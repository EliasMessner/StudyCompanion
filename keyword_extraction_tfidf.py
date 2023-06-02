from sklearn.feature_extraction.text import TfidfVectorizer

from data_integration_pipeline import pdf_to_str
from text_preprocessing import get_stopwords, clean_text


def get_search_terms(text, uni=4, bi=4, stop_words=None) -> str:
    """
    Returns unigrams and bigrams
    :param text: text to extract keywords from
    :param uni: number of unigrams to return
    :param bi: number of bigrams to return
    :param stop_words: stopwords to use
    :return: keywords as string (separated by space)
    """
    if stop_words is None:
        stop_words = get_stopwords("english", "german")
    top_bigrams = extract_keywords_from_text(text, n=bi, stop_words=stop_words, ngram_range=(2, 2))
    top_unigrams = [unigram for unigram in extract_keywords_from_text(text, n=uni, stop_words=stop_words,  ngram_range=(1, 1))
                    if not any(unigram in bigram for bigram in top_bigrams)]
    return ' '.join(top_unigrams + top_bigrams)


def extract_keywords_from_pdf(path_to_pdf, stop_words=None, n=5):
    if stop_words is None:
        stop_words = get_stopwords("german", "english")
    return extract_keywords_from_text(pdf_to_str(path_to_pdf), stop_words=stop_words, n=n)


def extract_keywords_from_text(text, n=5, stop_words=None, ngram_range=(1, 1)):
    if stop_words is None:
        stop_words = get_stopwords("english", "german")
    text_cleaned = clean_text(text, stop_words)
    kw_scores = get_keyword_scores(text_cleaned, ngram_range=ngram_range)
    return [kw[0] for kw in sorted(kw_scores.items(), key=lambda item: item[1], reverse=True)][:n]


def get_keyword_scores(text, ngram_range=(1, 1)):
    """
    Returns a dict mapping each unique token to its TF-IDF score
    """
    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(ngram_range=ngram_range)
    # Compute TF-IDF scores
    tfidf_matrix = vectorizer.fit_transform([text])
    # Get the feature names (tokens)
    feature_names = vectorizer.get_feature_names_out()
    # Create a dictionary of token to TF-IDF score
    keyword_scores = {}
    for col in tfidf_matrix.nonzero()[1]:
        keyword_scores[feature_names[col]] = tfidf_matrix[0, col]
    return keyword_scores
