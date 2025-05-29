import requests

url = "http://127.0.0.1:8000/scrape"
params = {
    "site": "bestbuy",
    "query": "Lenovo Tab P12-2024"
}

response = requests.get(url, params=params)
print("STATUS:", response.status_code)
print("TEXT:", response.text)
try:
    print("JSON:", response.json())
except Exception as e:
    print("ERROR:", e)
