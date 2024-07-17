
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('./malicious_phish.csv')  
# Ensure the dataset has the expected columns
assert 'url' in df.columns, "Dataset must have 'url' column"
assert 'type' in df.columns, "Dataset must have 'type' column"

# Feature extraction
df['url_length'] = df['url'].apply(len)
# Add more features if needed

# Define feature columns
feature_columns = ['url_length']  # Add more feature columns as needed

# Prepare the data
X = df[feature_columns]
y = df['type']  # Use 'type' as the label column

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, './trained_model.pkl')
