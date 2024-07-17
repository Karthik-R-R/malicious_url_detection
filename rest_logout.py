import requests

# URL for the logout endpoint
url = "http://127.0.0.1:8000/api/logout/"

# Replace with the actual access token you received during login
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwODkxOTkzLCJpYXQiOjE3MjA4OTE2OTMsImp0aSI6IjAxY2NhNDBhMDdlNTQ2ZGI5NWMwNzM1ZjhlZTU5YzFjIiwidXNlcl9pZCI6Mn0.GYRKNl3vDJoKv_sILdgMwntHixpjCSMTz-7RUsLlG68"

# Headers for the request
headers = {
    "Authorization": f"Bearer {access_token}",
}

# Send POST request
response = requests.post(url, headers=headers)

# Print response
if response.status_code == 200:
    print("Failed to log out")
    print(response.status_code, response.text)
else:
    print("User logged out successfully")
    print(response.json())