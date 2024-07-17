import requests

# URL for the login endpoint
login_url = "http://127.0.0.1:8000/api/login/"

# Prompt for admin credentials
admin_username = input("Enter admin username: ")
admin_password = input("Enter admin password: ")

# Admin user data to be sent in the request
login_data = {
    "username": admin_username,
    "password": admin_password
}

# Send POST request to login
login_response = requests.post(login_url, json=login_data)

# Check if login was successful
if login_response.status_code == 200:
    print("Admin logged in successfully")
    tokens = login_response.json()
    access_token = tokens.get("access")
    
    # URL for the list users endpoint
    list_users_url = "http://127.0.0.1:8000/api/admin/users/"
    
    # Headers for the request
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Send GET request to list users
    response = requests.get(list_users_url, headers=headers)
    
    # Print response
    if response.status_code == 200:
        print("Users listed successfully")
        print(response.json())
    else:
        print("Failed to list users")
        print(response.status_code, response.text)
else:
    print("Failed to log in")
    print(login_response.status_code, login_response.text)
