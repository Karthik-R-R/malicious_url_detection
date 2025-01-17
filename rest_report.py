# import requests

# # Define the endpoint URL
# url = 'http://127.0.0.1:8000/api/feedback/'

# # Define the feedback data
# feedback_data = {
#     'url': 'https://krishivhonda.com/',
#     'feedback_type': 'phishing',
#     'comment': 'This URL contains phishing content.'
# }

# # Make a POST request to submit the feedback
# response = requests.post(url, data=feedback_data)

# # Print the response status code and content
# print(f"Status Code: {response.status_code}")
# print("Response Content:")
# print(response.json())
import requests

# Define the URL of your API endpoint
url = 'http://127.0.0.1:8000/api/feedback/?url=http://chethan.com'

# Example data for feedback (adjust according to your model structure)
data = {
    'analysis': 1,  # Replace with the ID of the URLAnalysis object
    'is_correct': True,
    'user': 1,  # Replace with the ID of the User object
    # 'created_at' will be auto-generated by Django (auto_now_add=True)
}

# Send POST request
response = requests.post(url, data=data)

# Check the response
if response.status_code == 201:  # HTTP 201 Created
    print('Feedback successfully submitted!')
    print(response.json())  # Print the JSON response from the server
else:
    print(f'Failed to submit feedback. Status code: {response.status_code}')
    print(response.text)  # Print the error message from the server if any
