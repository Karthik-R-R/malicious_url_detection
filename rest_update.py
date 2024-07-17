import requests

# Define the base URL of your Django server
base_url = 'http://127.0.0.1:8000'

# Example analysis ID to update
analysis_id = 1

# Endpoint for updating URL analysis
url = f'{base_url}/api/analysis/{analysis_id}/'

# Example new URL string to update with
new_url_string = "https://example.com/new-url"

# Example request body
payload = {
    "url": new_url_string
}

# Example headers (if needed)
headers = {
    "Content-Type": "application/json",
    # Add any additional headers if required
}

# Send PUT request
response = requests.put(url, json=payload, headers=headers)

# Check the response
if response.status_code == 200:
    print("Analysis updated successfully")
    print(response.json())
else:
    print("Failed to update analysis")
    print(response.status_code, response.text)
