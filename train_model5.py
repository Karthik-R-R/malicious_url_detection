import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import re
from tqdm import tqdm

# Load the dataset
df = pd.read_csv('./malicious_phish.csv')  # Update with the correct path to your dataset

# dataset has the expected columns
assert 'url' in df.columns, "Dataset must have 'url' column"
assert 'type' in df.columns, "Dataset must have 'type' column"

# Feature extraction functions
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

# Apply feature extraction with progress tracking
tqdm.pandas(desc="Extracting features")
features_df = df['url'].progress_apply(extract_features).apply(pd.Series)

# Combine features with the original dataset
df = pd.concat([df, features_df], axis=1)

# Define feature columns
feature_columns = ['url_length', 'num_digits', 'num_letters', 'num_special_chars', 'num_subdomains', 'has_https', 'has_www']

# Prepare the data
X = df[feature_columns]
y = df['type']  
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model with progress tracking
model = RandomForestClassifier()
for i in tqdm(range(1), desc="Training model"):
    model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

# Save the model
joblib.dump(model, './trained_model.pkl')
