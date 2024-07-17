from sklearn.linear_model import SGDClassifier
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
import joblib

# Define the classes
classes = ['benign', 'malicious', 'phishing', 'malware']

# Initialize vectorizer and model
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3), max_features=10000)
model = SGDClassifier(loss='log_loss', random_state=42, max_iter=1000, tol=1e-3)

# Load the dataset in chunks
chunksize = 10000
for chunk in pd.read_csv('./malicious_phish.csv', chunksize=chunksize):
    X_chunk = vectorizer.fit_transform(chunk['url'])
    y_chunk = chunk['type']
    
    # Update classes dynamically
    unique_classes = y_chunk.unique()
    classes.extend([cls for cls in unique_classes if cls not in classes])
    
    # Partial fit with updated classes
    model.partial_fit(X_chunk, y_chunk, classes=classes)

# Save the model and vectorizer
joblib.dump(make_pipeline(vectorizer, model), './trained_model.pkl')
