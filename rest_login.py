
import requests

# URL for the login endpoint
url = "http://127.0.0.1:8000/api/login/"

# User data to be sent in the request
data = {
    "username": "admin",
    "password": "admin"
}

# Send POST request
response = requests.post(url, json=data)

# Print response
if response.status_code == 200:
    print("User logged in successfully")
    response_data = response.json()
    print("Access Token:", response_data.get('access'))
    print("Refresh Token:", response_data.get('refresh'))
else:
    print("Failed to log in")
    print(response.status_code, response.text)
