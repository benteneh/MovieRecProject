import requests

API_KEY = "6a9cfac6"
BASE_URL = "http://www.omdbapi.com/"

params = {
    "apikey": API_KEY,
    "t": "Inception"  
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}, {response.text}")

