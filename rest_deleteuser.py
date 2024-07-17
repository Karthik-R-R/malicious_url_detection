import requests

# URL for the delete user endpoint
user_id = 1  
url = f"http://127.0.0.1:8000/api/admin/user/2/"


admin_auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTQzMTg4LCJpYXQiOjE3MjA5NDI4ODgsImp0aSI6IjczZjM0Mzk1NDA1YTRmN2JiYzQ4MjVkODljMWQ1NDQ0IiwidXNlcl9pZCI6M30.GD96RFcz5yB-egoHFP_4EI4PuqIwBq0V2imI9N7yX8g"

# Headers for the request
headers = {
    "Authorization": f"Bearer {admin_auth_token}"
}

# Send DELETE request
response = requests.delete(url, headers=headers)

# Print response
if response.status_code == 200:
    print("User deleted successfully")
    print(response.json())
else:
    print("Failed to delete user")
    print(response.status_code, response.text)
