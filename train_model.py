# analysis/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load preprocessed data
df = pd.read_csv('D:/Edge Downloads/tech-tonic/project1/tech_tonic_hackathon/malicious_phish.csv')

# Feature and target selection
X = df[['url_length']]  
y = df['type'].apply(lambda x: 1 if x == 'malicious' else 0)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'path/to/trained_model.pkl')
