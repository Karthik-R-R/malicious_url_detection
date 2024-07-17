import requests

# URL for creating a new analysis
url = "http://127.0.0.1:8000/api/analysis/"

# data for analysis
data = {
    "url": "https://www.chethan1234.info",
    "probability": 0.95,  
    "user": 1 
}

# Send POST request
response = requests.post(url, data=data)

# Print response
if response.status_code == 201:
    print("Analysis added successfully")
    print(response.json())
else:
    print("Failed to add analysis")
    print(response.status_code, response.text)
