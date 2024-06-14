import requests
import json

url = "http://localhost:8080/detect"

data_to_send = {
    "scenario": "D"
}

file_path = "C:/Users/PRALANITED01/Pictures/img_prueba.jpg"

image_file = {"image_file": ("img_prueba.jpg", open(file_path, "rb"), "image/jpeg")}

response = requests.post(url, data=data_to_send, files=image_file)

if response.status_code == 200:
    print("Successful request. Server response:")
    # print(response.text)
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Request failed with status code {response.status_code}")

