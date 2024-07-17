import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

# Load the dataset
df = pd.read_csv('./malicious_phish.csv')  # Update with the correct path to your dataset

# Feature extraction
# Use TfidfVectorizer to convert URLs to numerical features
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 5))

# Prepare the data
X = vectorizer.fit_transform(df['url'])
y = df['type']  # Use 'type' as the label column

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f'Model accuracy: {accuracy * 100:.2f}%')

# Save the model and vectorizer
joblib.dump(make_pipeline(vectorizer, model), './trained_model.pkl')
