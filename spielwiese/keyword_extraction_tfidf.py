from langchain.document_loaders import PyPDFLoader
from sklearn.feature_extraction.text import TfidfVectorizer

from text_preprocessing import get_stopwords, clean


def extract_keywords_from_pdf(path_to_pdf, stop_words=None, n=5):
    if stop_words is None:
        stop_words = get_stopwords("german", "english")
    return extract_keywords_from_text(pdf_to_str(path_to_pdf), stop_words=stop_words, n=n)


def extract_keywords_from_text(text, n=5, stop_words=None):
    if stop_words is None:
        stop_words = get_stopwords("english", "german")
    text_cleaned = clean(text, stop_words)
    kw_scores = get_keyword_scores(text_cleaned)
    return sorted(kw_scores.items(), key=lambda item: item[1], reverse=True)[:n]


def get_keyword_scores(text):
    """
    Returns a dict mapping each unique token to its TF-IDF score
    """
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


def pdf_to_str(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return ' '.join(doc.page_content for doc in documents)
