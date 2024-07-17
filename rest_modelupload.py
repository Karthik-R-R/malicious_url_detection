import requests

# URL for the upload model endpoint
url = "http://127.0.0.1:8000/api/model/"

# Replace with the path to your model file
model_file_path = "./trained_model_new.pkl"

# Open the model file
with open(model_file_path, 'rb') as model_file:
    files = {
        'modelFile': model_file
    }

    # Send POST request with the file
    response = requests.post(url, files=files)

    # Print response
    if response.status_code == 201:
        print("Model uploaded successfully")
        print(response.json())
    else:
        print("Failed to upload model")
        print(response.status_code, response.text)
