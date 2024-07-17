
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

# Define your pipeline components
tfidf_vectorizer = TfidfVectorizer()
classifier = SGDClassifier()

# Construct the pipeline
model = Pipeline([
    ('tfidf', tfidf_vectorizer),
    ('clf', classifier),
])
