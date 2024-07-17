import requests

# URL for deleting an analysis 
analysis_id = 1  # Replace with the ID of the analysis you want to delete
url = f"http://127.0.0.1:8000/api/analysis/{analysis_id}/"

# Headers if needed 
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTQzMTg4LCJpYXQiOjE3MjA5NDI4ODgsImp0aSI6IjczZjM0Mzk1NDA1YTRmN2JiYzQ4MjVkODljMWQ1NDQ0IiwidXNlcl9pZCI6M30.GD96RFcz5yB-egoHFP_4EI4PuqIwBq0V2imI9N7yX8g"  # Replace with your actual auth token if required
}

# Send DELETE request
response = requests.delete(url, headers=headers)

# Print response
if response.status_code == 204:
    print(f"Analysis {analysis_id} deleted successfully")
else:
    print(f"Failed to delete analysis {analysis_id}")
    print(response.status_code, response.text)
