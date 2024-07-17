import requests

# Define the URL for the registration endpoint
url = 'http://127.0.0.1:8000/api/register/'

# Define the registration data
data = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin"
}

# Send the POST request to the registration endpoint
response = requests.post(url, json=data)

# Check the response status code and print the response
if response.status_code == 201:
    print("Registration successful!")
    print("Response:", response.json())
else:
    print("Registration failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.json())
