
import joblib
import os
from urllib.parse import urlparse
from .pipeline import model
import joblib
import re
import pandas as pd


# Determine the path to the trained model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'tech_tonic_hackathon', 'trained_model.pkl')

# Load the trained model
model = joblib.load(model_path)

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_letters'] = sum(c.isalpha() for c in url)
    features['num_special_chars'] = len(re.findall(r'\W', url))
    features['num_subdomains'] = url.count('.') - 1
    features['has_https'] = int('https' in url)
    features['has_www'] = int('www' in url)
    return features

#Function to analyze the URL
def analyze_url(url):
    # Extract features from the URL
    features_dict = extract_features(url)
    
    # Convert the features to DataFrame to match the model input format
    features_df = pd.DataFrame([features_dict])
    
    # Predict using the trained model
    prediction = model.predict(features_df)
    
    return prediction[0]
