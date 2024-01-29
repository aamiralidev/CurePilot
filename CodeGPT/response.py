import requests

data = {"Name": "Aasif", "Age": 22, "Country": "Pakistan"}
response = requests.post("http://127.0.0.1:8000/codegpt", json=data)
print(response.json())
